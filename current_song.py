import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
	client_id=CLIENT_ID, 
	client_secret=CLIENT_SECRET,
	cache_path='../.cache-willfurtado',
	redirect_uri=REDIRECT_URI))

try:
	curr_song_meta = sp.currently_playing(market=None)
	curr_song_name, curr_artist_name = curr_song_meta['item']['name'], curr_song_meta['item']['artists'][0]['name']
	curr_user = sp.current_user()['display_name']
	print("\n" * 5, curr_user, "is listening to {} by {}".format(curr_song_name, curr_artist_name))
	print("\n" * 5)
	
except:
	curr_user = sp.current_user()['display_name']
	print("\n" * 5, curr_user, "is not listening to any songs right now.")
	print("\n" * 5)


