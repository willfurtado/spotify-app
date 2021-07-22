import argparse

import spotipy
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("time_range")
    flags = parser.parse_args()

    scope = "user-top-read"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
    )

    num_top = int(input("How many of your tops: "))

    user = sp.current_user()["display_name"]

    top_songs = sp.current_user_top_tracks(limit=num_top, time_range=flags.time_range)

    print(f"\n\nTop {num_top} {flags.time_range} songs for {user}")
    print(50 * "-")

    for i in range(num_top):
        try:
            song = top_songs["items"][i - 1]
            print(
                f"{i + 1}: {song['name']} -- {song['duration_ms'] / 3600} minutes listened"
            )
        except IndexError:
            print(f"Less than {num_top} top songs; occured at number {i}")
            break

    top_artists = sp.current_user_top_artists(
        limit=num_top, time_range=flags.time_range
    )

    print(f"\n\nTop {num_top} {flags.time_range} artists for {user}")
    print(50 * "-")

    for i in range(num_top):
        try:
            artist = top_artists["items"][i]
            print(
                f"{i + 1}: {artist['name']} -- Genre: {artist['genres']}",
            )
        except IndexError:
            print(f"Less than {num_top} top artists; occured at number {i}")
            break
