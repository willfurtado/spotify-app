import spotipy
import json
import base64
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

REDIRECT_URI = "https://google.com/"
scope = "playlist-modify-public ugc-image-upload"
IMG_PATH = "cover_photos/green.jpg"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET,
    cache_path='../.cache-willfurtado',
    redirect_uri=REDIRECT_URI))

def get_spotify_uri(song):
    """
    Returns the corresponding spotify URI from a given song title
    """
    search_results = sp.search(q=str(song + "%20"), type='track', limit=1)
    try:
        return search_results['tracks']['items'][0]['id']
    except (AttributeError, IndexError) as err:
        print('No results for {}'.format(song))
    
def getCurrentUser():
    """
    Returns the username of the current user.
    """
    try:
        return sp.current_user()['display_name']
    except:
        print("Could not get Current User information.")

def getNewPlaylistURI():
    """
    Returns the spotify URI of the current user's most recent playlist
    """
    try:
        return sp.current_user_playlists()['items'][0]['uri']
    except:
        print("Could not get URI of latest Spotify playlist.")

def promptUserInput():
    """
    Prompts for user input and will create a dictionary with corresponding song URI codes
    """
    tracks = {}
    sentence_string = input("Write a sentence: ")
    words = sentence_string.lower().split()
    for word in words:
        track_id = get_spotify_uri(word)
        if word not in tracks:
            tracks[word] = track_id
    return tracks

def uploadPlaylistCover(playlist_id):
    """
    Uploads the Base 64 encoded image to the playlist
    """
    with open(IMG_PATH, "rb") as image_file:
        im = base64.b64encode(image_file.read())
    sp.playlist_upload_cover_image(playlist_id, im)


def playlistGenerator():
    """
    Creates a generated playlist
    """
    tracks = promptUserInput()
    sp.user_playlist_create(getCurrentUser(), 
            "Sing me a bedtime story...", 
            public=True, 
            description="This playlist was automatically generated based on user input using the Spotify Web API. See the code on GitHub! @willfurtado")
    
    playlist_id = getNewPlaylistURI()
    uploadPlaylistCover(playlist_id)
    tracks_list = list(tracks.values())
    sp.user_playlist_add_tracks(getCurrentUser(), 
                                playlist_id, 
                                tracks_list)

    return "Playlist created successfully!"

playlistGenerator()