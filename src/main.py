"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {"genre": "metal", "mood": "romantic", "energy": 0.7, "likes_acoustic": False}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("  Top Recommendations")
    print("=" * 40)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}: {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Why:")
        for reason in explanation.split(" | "):
            print(f"      - {reason}")

    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
