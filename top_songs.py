import spotipy
import json
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
	client_id=CLIENT_ID, 
	client_secret=CLIENT_SECRET,
	cache_path='../.cache-willfurtado',
	redirect_uri=REDIRECT_URI))

time_range=str(input('Time Range (either short_term, medium_term, long_term: '))

top_songs = sp.current_user_top_tracks(limit=25, time_range=time_range)

user=sp.current_user()['display_name']
print("\n {} TOP SONGS FOR {}".format(time_range, user))

for i in range(1,26):
	print('\n')
	song = top_songs['items'][i-1]
	print("{}:".format(i), song['name'], "-- {} minutes listened".format(round(song['duration_ms'] / 3600), 2))
