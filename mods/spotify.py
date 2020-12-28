import asyncio
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#config loading libs
import os.path
import qtoml as toml


def get_spotify_client(path=os.path.join('C2_Bot', 'mods', 'configs', 'spotify.toml')):
    with open(path, 'r') as f:
        config = toml.load(f)
    os.environ['SPOTIPY_CLIENT_ID'] = config['spotify']['SPOTIPY_CLIENT_ID']
    os.environ['SPOTIPY_CLIENT_SECRET'] = config['spotify']['SPOTIPY_CLIENT_SECRET']
    os.environ['SPOTIPY_REDIRECT_URI'] = config['spotify']['SPOTIPY_REDIRECT_URI']
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    return spotify_client

async def spotify_search(message, spotify_client = get_spotify_client()):
    '''Spotify searching function that returns the first 5 spotify urls for a search type'''
    search_raw = message.content.split()
    if search_raw[1] in ['track', 'album', 'artist', 'playlist']:
        search_type = search_raw[1]
        search_query= " ".join(search_raw[2:])
    else:
        search_type = 'track'
        search_query= " ".join(search_raw[1:])
    search_results = spotify_client.search(search_query, type = search_type, limit=5)
    search_result_urls = []
    for i in range(0, 5):
        search_result_urls.append(search_results['{st}s'.format(st=search_type)]['items'][i]['external_urls']['spotify'])
    await message.channel.send('{0}\n{1}\n{2}\n{3}\n{4}\nThese are the top 5 results for your {t} search: "{c}"'.format(search_result_urls[0], search_result_urls[1], search_result_urls[2], search_result_urls[3], search_result_urls[4], t=search_type, c=search_query))

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}
help = {'spotify_search' : ''}
