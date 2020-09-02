import spotipy
import json
import pandas as pd
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
	client_id=CLIENT_ID, 
	client_secret=CLIENT_SECRET,
	username='willfurtado',
	redirect_uri=REDIRECT_URI))

num_top = int(input("Number of Songs, Artists:"))

top_songs = sp.current_user_top_tracks(limit=num_top, time_range="long_term")
top_artists = sp.current_user_top_artists(limit=num_top, time_range="long_term")
user=sp.current_user()['display_name']

print("\n\n\n              {} top artists for {}".format(num_top, user))

d = {'Artist':[], 'Genre':[]}
for i in range(num_top):
	try:
		artist = top_artists['items'][i]['name']
		genres = top_artists['items'][i]['genres']

		d['Artist'].append(artist)
		d['Genre'].append(genres)

	except IndexError as err:
		print("Less than {} top artists; occured at number {}".format(num_top, i))
		break

df = pd.DataFrame(d)
print(df)

genre_dict = {}

for i in range(num_top):
	try:
		genres = top_artists['items'][i]['genres']
		for genre in genres:
			genre_dict[genre] = 1 + genre_dict.get(genre, 0)

	except IndexError as err:
		print("Less than {} top artists; occured at number {}".format(num_top, i))
		break
genre_tbl = {"Genre": list(genre_dict.keys()), "Count": list(genre_dict.values())}
#print(json.dumps(genre_tbl, indent=2))
genre_df = pd.DataFrame(genre_tbl).sort_values("Count", ascending=False).reset_index(drop=True)
print(genre_df)
