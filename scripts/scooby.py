import spotipy
import json
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

if __name__ == "__main__":

    scope = "user-top-read"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
    )

    scooby_features = sp.audio_features(
        tracks=["spotify:track:4SVNBpvhXu8agkCRqWl09o"]
    )[0]
    print("\n           Audio Analysis of Scooby:\n")
    print(json.dumps(scooby_features, indent=2))
    print("\n")
