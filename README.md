# 🎵 FindBeats

## Original Project Summary

Original project is Project 3 - Music Recommender Simulation
Goal of original project: provide user 5 song recommendations that match their personal music preference, taking into account their preferred genre, mood, energy level, and whether they like acousticness or not based on a scoring rule. The user had to know exactly what genre, mood, and energy level they wanted

---

## Final Project Summary - FindBeats

The original project was refined to use RAG to retrieve information from songs.csv to provide the user with song recommendations that match their preferences - either provided from a sidebar panel or simply through chatting with the tool. The extract_prefs function understands the user's preferences, recommend_songs works to apply the scoring rule and retrieves the songs from songs.csv, and the LLM generates the response provided to the user.
This change from the previous project is important as it now provides the user the option to simply chat with the system instead of knowing exactly the genre, mood, and energy level they wanted. 
---

## Architecture Overview

The user can chat with the system or use the sidebar on the left to select their preferences. As soon as the user sends a message, extract_prefs reads it and determines the genre, mood, and energy level. Those preferences are  passed to recommend_songs, which scores every song in songs.csv using the scoring rule and returns the top 5 songs with reasons. The retrieved songs are then formatted into a context block by build_context and injected directly into the prompt sent to qwen2.5:1.5b. The LLM reads that context and generates a response using the retrieved songs.
---
## Sample Interactions

Sample run 1- User prompt: I want some tracks that are chill for studying.

![Sample Run 1](assets/Sample%20run%201-using%20chat.png)

Sample run 2- User prompt (using sidebar): genre: lofi, mood: sad, energy level: 0.3

![Sample Run 2](assets/Sample%20run%202-using%20sidebar.png)
---

## Design Decisions

- I chose to use Ollama instead of a cloud model because it is free and doesn't need an API key. However, a trade off is the speed. It runs much slower than a cloud model.
- I chose to include a UI for this because previously it was a command line application, and I wanted it to be more iteractive for the user. I chose to include a sidebar panel as well as a chat option so the user can use either of the two options to convey their preferences.
---
## Testing Summary

**What worked:**
- The scoring algorithm (recommend_songs) worked correctly and was verified with pytest — genre match, mood match, energy similarity, and acoustic preference all scored as expected
- RAG returned real songs from songs.csv every time, with no hallucinations
- The sidebar panel produces consistent results since preferences are passed directly as structured text
- findbeats.log confirms that RAG works correctly before every response

**What didn't work:**
- qwen2.5:0.5b was too small — it generated placeholder text instead of actually using the retrieved songs and qwen2.5:3b, a larger model worked but it was too slow so a qwen2.5:1b was used 
- Tool-calling RAG (where the LLM decides when to call search_songs) failed because small models skipped the tool call completely


**What I learned:**
- Small models can be unreliable for tool use 
- The LLM's role in this system is generation only — all retrieval and scoring logic should stay in Python
---
## Reflection

This project helped me gain an understanding of how AI models behave, and how its the job of the human to make architecture and design decisions in order to ensure the system works as intended. The smaller AI model was fast, but it wasn't reliable, but the bigger one was too slow, but provided accurate responses. And so, this project showed me that AI can work unexpectedly and so it is necessary to keep a human in the loop who can problem solve and make decisions that can prevent errors. An important debugging and problem solving method I gained from this project was to use logs to understand how the AI was working in the background, which allowed me to immediately understand that a certain function wasn't being called at all, requiring me to change my design. I also gained an indepth understanding of how real music recommendation apps like Spotify work. 
---
## System Diagram

![System Design](assets/System%20design.png)

**Data flow:**
- **Input** — user types naturally or fills in the sidebar form
- **Retrieve** — `extract_prefs` reads the user message and determines genre, mood, and energy; `recommend_songs` immediately scores and retrieves the top 5 songs from `songs.csv`
- **Augment** — `build_context` formats the retrieved songs and their scoring reasons into a prompt the LLM can read
- **Generate** — the LLM receives the augmented prompt and writes a response using only the retrieved data
- **Output** — grounded response with real song titles, artists, and reasons from the catalog
- **Logging** — every retrieval and generation step is written to `findbeats.log`
- **Testing** — pytest covers the scoring logic; humans verify output quality via logs

---

## Getting Started

### Requirements

- Python 3.10+
- [Ollama](https://ollama.com) (free, runs AI locally — no API key needed)

### Setup

1. Install [Ollama](https://ollama.com) and pull the model:

   ```bash
   ollama pull qwen2.5:1.5b
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac / Linux
   .venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

   The app will open automatically in your browser at `http://localhost:8501`.

> **Note:** Make sure Ollama is running in the background before starting the app.  
> On Windows it starts automatically after installation. On Mac/Linux run `ollama serve`.

### Logs

The app writes logs to `findbeats.log` in the project root. This tracks every tool call, fallback event, and error for debugging.

### Running Tests

```bash
pytest
```


