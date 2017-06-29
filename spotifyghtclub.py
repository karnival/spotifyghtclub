import credentials
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util
import json
import os.path

def get_playlist_tracks(username, playlist_id):
	results = sp.user_playlist_tracks(username, playlist_id)
	tracks = results['items']
	while results['next']:
		results = sp.next(results)
		tracks.extend(results['items'])
	return tracks

client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id, client_secret=credentials.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

uri = 'spotify:user:2000trees:playlist:4y8CMp96xX3fEbSkKUiRty'

username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

playlist_filename = playlist_id + '.json'

if os.path.isfile(playlist_filename):
	print('file found')
	with open(playlist_filename, 'r') as infile:
		tracks = json.load(infile)
else:
	print('file not found')
	tracks = get_playlist_tracks(username, playlist_id)
	with open(playlist_filename, 'w') as outfile:
		json.dump(tracks, outfile)

for t in tracks:
	#print(t["track"]["name"])
	pass


my_uri = 'spotify:user:ransaccc:playlist:5qcEczOgABfkROHMqbGfUX'
username = my_uri.split(':')[2]
playlist_id = my_uri.split(':')[4]
track_ids = ['03p52fO3w4RrRnnEqAAM0w']

scope = 'playlist-modify-public'
token = spotipy.util.prompt_for_user_token(username, scope, client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri='http://localhost:8888/callback')

sp = spotipy.Spotify(auth=token)
results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
print(results)
