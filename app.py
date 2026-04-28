import logging
import streamlit as st
import ollama
from src.recommender import load_songs, recommend_songs

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("findbeats.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── Load catalog ──────────────────────────────────────────────────────────────
try:
    songs = load_songs("data/songs.csv")
    log.info("Loaded %d songs from catalog.", len(songs))
except FileNotFoundError:
    st.error("Song catalog not found. Make sure `data/songs.csv` exists.")
    st.stop()

MODEL  = "qwen2.5:1.5b"
GENRES = ["pop", "lofi", "rock", "ambient", "jazz", "synthwave", "indie pop",
          "hip-hop", "classical", "country", "r&b", "metal", "blues", "j-pop", "electronic"]
MOODS  = ["happy", "chill", "intense", "relaxed", "moody",
          "focused", "nostalgic", "sad", "angry", "romantic"]


# ── Retrieval ─────────────────────────────────────────────────────────────────
def extract_prefs(text: str) -> dict:
    t = text.lower()
    genre  = next((g for g in GENRES if g in t), "lofi")
    mood   = next((m for m in MOODS  if m in t), "chill")
    energy = 0.3 if any(w in t for w in ["chill", "relax", "study", "focus", "sleep", "calm"]) else 0.6
    acoustic = any(w in t for w in ["acoustic", "unplugged"])
    return {"genre": genre, "mood": mood, "energy": energy, "likes_acoustic": acoustic}


def retrieve(prefs: dict) -> list:
    results = recommend_songs(prefs, songs, k=5)
    log.info("Retrieved songs — genre=%s, mood=%s, energy=%.1f",
             prefs["genre"], prefs["mood"], prefs["energy"])
    return [
        {"title": s["title"], "artist": s["artist"],
         "genre": s["genre"], "mood": s["mood"], "energy": s["energy"],
         "reasons": explanation}
        for s, _, explanation in results
    ]


def build_context(results: list) -> str:
    lines = []
    for i, s in enumerate(results, 1):
        lines.append(
            f"{i}. \"{s['title']}\" by {s['artist']} "
            f"[{s['genre']}, {s['mood']}, energy {s['energy']}] — {s['reasons']}"
        )
    return "\n".join(lines)


# ── Generation ────────────────────────────────────────────────────────────────
def get_reply(user_message: str) -> str:
    # Step 1 — Retrieve
    prefs   = extract_prefs(user_message)
    results = retrieve(prefs)
    context = build_context(results)
    log.info("Injecting %d songs into prompt.", len(results))

    # Step 2 — Augment prompt with retrieved data
    prompt = f"""\
You are FindBeats, a friendly music recommendation assistant.

The user said: "{user_message}"

Based on their request, here are the 5 most relevant songs retrieved from the catalog:
{context}

Using ONLY the songs listed above, write a friendly response that:
- Presents all 5 songs with their title and artist (use the exact names above)
- For each song, explain in plain English why it fits the user's request using the reasons provided
- Do not invent any songs or reasons not in the list above
"""

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        reply = response.message.content
        log.info("Model generated response successfully.")
        return reply
    except ollama.ResponseError as e:
        log.error("Ollama error: %s", e)
        if "not found" in str(e).lower():
            return f"Model `{MODEL}` not found. Run `ollama pull {MODEL}` and refresh."
        return f"AI error: {e}"
    except Exception as e:
        log.error("Unexpected error: %s", e)
        return "Something went wrong. Make sure Ollama is running and try again."


def send_message(prompt: str):
    if not prompt.strip():
        return
    log.info("User message: %s", prompt)
    st.session_state.display.append({"role": "user", "content": prompt})
    reply = get_reply(prompt)
    st.session_state.display.append({"role": "assistant", "content": reply})


# ── Session state ─────────────────────────────────────────────────────────────
if "display" not in st.session_state:
    st.session_state.display = [{
        "role": "assistant",
        "content": "Hi! I'm FindBeats. Use the sidebar to set your preferences, or just tell me what you want to listen to.",
    }]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Music Preferences")
    genre          = st.selectbox("Favorite Genre", GENRES)
    mood           = st.selectbox("Favorite Mood", MOODS)
    energy         = st.slider("Energy Level", 0.0, 1.0, 0.5, 0.1,
                                help="0 = very chill, 1 = high energy")
    likes_acoustic = st.checkbox("Prefer acoustic songs")

    if st.button("Find Songs", use_container_width=True, type="primary"):
        acoustic_str = "acoustic" if likes_acoustic else "non-acoustic"
        prompt = (f"Find me {genre} songs with a {mood} mood, "
                  f"energy level around {energy}, and I prefer {acoustic_str} tracks.")
        with st.spinner("Finding songs for you..."):
            send_message(prompt)
        st.rerun()

# ── Main chat ─────────────────────────────────────────────────────────────────
st.title("🎵 FindBeats")
st.caption("Use the sidebar or just chat to find your perfect playlist.")

for msg in st.session_state.display:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Or just tell me what you're feeling..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Finding songs for you..."):
            send_message(prompt)
        st.write(st.session_state.display[-1]["content"])
