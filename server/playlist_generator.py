import spotipy
import json
import base64
import spacy
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from spacy.lang.en import English

REDIRECT_URI = "https://google.com/"
scope = "playlist-modify-public ugc-image-upload"
IMG_PATH = "cover_photos/green.jpg"
nlp = spacy.load("en_core_web_sm")
nlp = English()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET,
    cache_path='../.cache-willfurtado',
    redirect_uri=REDIRECT_URI))

def get_spotify_uri(song):
    """
    Returns the corresponding spotify URI from a given song title
    """
    try:
        results = sp.search(q=song, type="track", limit=50)['tracks']['items']
        names, ids = [results[i]['name'] for i in range(50)], [results[i]['id'] for i in range(50)]
        zipped, zipped2 = zip(names, ids), zip(names, ids)
        perfect_match = [track_id for (name, track_id) in zipped2 if name.lower() == song.lower()]
        track_uri = [track_id for (name, track_id) in zipped if name.lower().startswith(song.lower() + " ")][0]
        return track_uri if not perfect_match else perfect_match[0]
    except (AttributeError, IndexError) as err:
        return err
    
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

def parseUserInput(sentence):
    """
    Prompts for user input and will create a dictionary with corresponding song URI codes
    """
    tracks = {}
    tokens = nlp(sentence)
    for token in tokens:
        track_id = get_spotify_uri(token.text)
        if token.text not in tracks:
            tracks[token.text] = track_id
    return tracks

def uploadPlaylistCover(playlist_id):
    """
    Uploads the Base 64 encoded image to the playlist
    """
    with open(IMG_PATH, "rb") as image_file:
        im = base64.b64encode(image_file.read())
    sp.playlist_upload_cover_image(playlist_id, im)


def playlistGenerator(sentence):
    """
    Creates a generated playlist
    """
    tracks = parseUserInput(sentence)
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

    return sp.playlist(playlist_id)['external_urls']['spotify']
