import requests
import cPickle as pickle
import pprint
import json
import os
import plotly.plotly 
import spotify_helper as sh
import plotly.graph_objs as go

USER = os.environ['SPOTIFY_USER_ID']

playlists = sh.get_user_playlists(USER)
artists = {}
for current_playlist in playlists:
  playlist_tracks = sh.call_user_playlist_tracks_api(USER, current_playlist ['id'])

  if playlist_tracks is None:
    print "Playlist not received: {playlist_id}".format(playlist_id = current_playlist ['id'])
    continue

  for t in playlist_tracks:
    track = t['track']
    album = track['album']
    track_artists = track['artists']

    for artist in track_artists:
      artist_id = artist['id']
      if artist_id not in artists:
        artists[artist_id] = {
          'id': artist['id'],
          'name': artist['name'],
          'ref_count': 0
        }

      artists[artist_id]['ref_count'] += 1


pprint.pprint(artists)

x_axis = []
y_axis = []
text = []
#x_axis = [x['name'] for x in artists]
#y_axis = [x['ref_count'] for x in artists]
#text = [x['name'] for x in artists]
for artist, artist_data in artists.iteritems():
    print "********** ARTIST ****************"
    pprint.pprint(artist)
    pprint.pprint(artist_data)
    x_axis.append(artist_data['name'])
    y_axis.append(artist_data['ref_count'])
    text.append(artist_data['name'])

trace0 = go.Bar(
    x=x_axis,
    y=y_axis,
    text=text,
    marker=dict(
        color='rgb(158,202,225)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5,
        )
    ),
    opacity=0.6
)
data = [trace0]
layout = go.Layout(
    title='Spotify Playlist Artist Counter for ' + str(USER),
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)
