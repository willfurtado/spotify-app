import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import spotipy
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

    num_top = int(input("Number of Songs, Artists:"))

    top_songs = sp.current_user_top_tracks(
        limit=num_top,
        time_range="long_term",
    )
    top_artists = sp.current_user_top_artists(
        limit=num_top,
        time_range="long_term",
    )
    user = sp.current_user()["display_name"]

    print(f"\n\n\n              {num_top} top artists for {user}")

    d = {"Artist": [], "Genre": []}
    for i in range(num_top):
        try:
            artist = top_artists["items"][i]["name"]
            genres = top_artists["items"][i]["genres"]

            d["Artist"].append(artist)
            d["Genre"].append(genres)

        except IndexError:
            print(f"Less than {num_top} top artists; occured at number {i}")
            break

    df = pd.DataFrame(d)
    print(df)

    genre_dict = {}

    for i in range(num_top):
        try:
            genres = top_artists["items"][i]["genres"]
            for genre in genres:
                genre_dict[genre] = 1 + genre_dict.get(genre, 0)

        except IndexError:
            print(f"Less than {num_top} top artists; occured at number {i}")
            break
    genre_tbl = {"Genre": list(genre_dict.keys()), "Count": list(genre_dict.values())}

    genre_df = (
        pd.DataFrame(genre_tbl)
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )
    print(genre_df)
    vis_df = genre_df.head(10)
    plt.figure(figsize=(5, 5))
    sns.barplot(x="Count", y="Genre", data=vis_df, orient="h", palette="plasma")
    plt.show()
