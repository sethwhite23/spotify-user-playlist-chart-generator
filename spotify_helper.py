import requests
import pprint
import json
import os
import datetime

SPOTIFY_TOKEN = None

def get_spotify_token():
  global SPOTIFY_TOKEN

  current_time = datetime.datetime.now()

  if SPOTIFY_TOKEN is None or current_time > SPOTIFY_TOKEN['expiration']:
    url = "https://accounts.spotify.com/api/token"

    payload = {
              'grant_type': 'client_credentials'
              }
    
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    
    auth = (client_id, client_secret)
    response = requests.post(url, data=payload, auth = (client_id, client_secret))

    if response.status_code != 200:
      raise Exception("Error getting spotify token!")

    response_data = json.loads(response.text)

    expiration_time = current_time + datetime.timedelta(0,int(response_data['expires_in']))

    SPOTIFY_TOKEN = {
      'access_token': response_data['access_token'],
      'expiration': expiration_time 
    }

    #print "SPOTIFY TOKEN"
    #pprint.pprint(SPOTIFY_TOKEN)

  return SPOTIFY_TOKEN

def get_user_playlists(user):
  limit = 50
  offset = 0
  token = get_spotify_token()
  url = "https://api.spotify.com/v1/users/{user}/playlists?limit={limit}&offset={offset}".format(user=user, limit = limit, offset = offset)
  headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer {token}'.format(token = token['access_token'])
  }

  user_playlists = []

  next_url = url
  while True:
    print "NEXT URL: " + next_url
    response = requests.get(next_url, headers=headers)

    if response.status_code != 200:
      print "ERROR OCCURED IN PLAYLIST:"
      pprint.pprint(response)
      return None
      break

    response_json = response.json()
    playlists = response_json['items']

    for p in playlists:
      playlist = {}
      playlist['id'] = p['id'] 
      playlist['name'] = p['name']
      playlist['snapshot_id'] = p['snapshot_id']
      user_playlists.append(p)

    next_url = response_json['next']

    if next_url is None:
      break

  return user_playlists

def call_user_playlist_tracks_api(user_id, playlist_id):
  token = get_spotify_token()
  url = "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks".format(user_id = user_id, playlist_id = playlist_id)

  print "URL " + url
  headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer {token}'.format(token = token['access_token'])
  }
  response = requests.get(url, headers=headers)
  
  if response.status_code != 200:
      print "ERROR OCCURED IN TRACKS:"
      pprint.pprint(response)
      print "Response Text"
      print response.text
      return None

  response_json = response.json()
  tracks = response_json['items']

  return tracks


get_user_playlists('sethwhite23')
