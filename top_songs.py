import spotipy
import json
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        cache_path=".cache-willfurtado",
        redirect_uri=REDIRECT_URI,
    )
)

time_range = str(input("Time Range (either short_term, medium_term, long_term: "))
num_top = int(input("How many of your tops: "))
top_songs = sp.current_user_top_tracks(limit=num_top, time_range=time_range)
top_artists = sp.current_user_top_artists(limit=num_top, time_range=time_range)
user = sp.current_user()["display_name"]

print("\n\n\n              {} top {} songs for {}".format(num_top, time_range, user))

for i in range(num_top):
    try:
        print("\n")
        song = top_songs["items"][i - 1]
        print(
            "{}:".format(i + 1),
            song["name"],
            "-- {} minutes listened".format(round(song["duration_ms"] / 3600), 2),
        )
    except IndexError:
        print("Less than {} topsongs; occured at number {}".format(num_top, i))
        break

print("\n\n\n              {} top {} artists for {}".format(num_top, time_range, user))

for i in range(num_top):
    try:
        print("\n")
        artist = top_artists["items"][i]
        print(
            "{}:".format(i + 1),
            artist["name"],
            "-- Genre: {}".format((artist["genres"])),
        )
    except IndexError:
        print("Less than {} top artists; occured at number {}".format(num_top, i))
        break
