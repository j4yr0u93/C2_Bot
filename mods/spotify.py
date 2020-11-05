import asyncio
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#init
import os.path
import qtoml as toml

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
        return config

config = load_config(os.path.join('C2_Bot', 'mods', 'configs', 'spotify.toml'))
spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = config['spotify']['SPOTIPY_CLIENT_ID'], client_secret = config['spotify']['SPOTIPY_CLIENT_SECRET']))

async def spotify_search(message):
    '''Passes literal input to spotify.search() function'''
    search_raw = message.content.split()
    search_query = " ".join(search_raw[1:])
    search_results = spotify_client.search(search_query)
#    result_url = search_results.get('external_urls')
    await message.channel.send(search_results)

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}
