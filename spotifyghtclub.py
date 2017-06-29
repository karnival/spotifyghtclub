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

def add_track_to_playlist(track_ids):
	my_uri = 'spotify:user:ransaccc:playlist:5qcEczOgABfkROHMqbGfUX'
	username = my_uri.split(':')[2]
	playlist_id = my_uri.split(':')[4]
	
	scope = 'playlist-modify-public'
	token = spotipy.util.prompt_for_user_token(username, scope, client_id=credentials.client_id, client_secret=credentials.client_secret, redirect_uri='http://localhost:8888/callback')
	
	sp = spotipy.Spotify(auth=token)
	results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
	print(results)

def get_new_track_for_artist(artist, track_ids_old, track_names_old):
	# Get a track, from artist's top tracks, that wasn't in the old playlist.
	response = sp.artist_top_tracks('spotify:artist:' + artist)
	
	for track in response['tracks']:
		if track['id'] not in track_ids_old and track['name'] not in track_names_old:
			track_new = track['id']
			break
	return track_new
			

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

track_ids = []
artist_ids = []
track_names = []
for t in tracks:
	track_ids.append(t['track']['id'])
	track_names.append(t['track']['name'])
	artist_ids.append(t['track']['artists'][0]['id'])

tracks_to_add = []
for a in artist_ids:
	t_new = get_new_track_for_artist(a, track_ids, track_names)
	tracks_to_add.append(t_new)

tracks_to_add_dedup = set(tracks_to_add)

add_track_to_playlist(tracks_to_add_dedup)
