import asyncio
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#config loading libs
import os.path
import qtoml as toml

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
        return config

def get_spotify_client():
    config = load_config(os.path.join('C2_Bot', 'mods', 'configs', 'spotify.toml'))
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = config['spotify']['SPOTIPY_CLIENT_ID'], client_secret = config['spotify']['SPOTIPY_CLIENT_SECRET']))
    return spotify_client

async def spotify_search(message):
    '''Passes literal input to spotify.search() function'''
    spotify_client = get_spotify_client()
    search_raw = message.content.split()
    search_query = " ".join(search_raw[1:])
    search_results = spotify_client.search(search_query)
#    result_url = search_results.get('external_urls')
    await message.channel.send(search_results)

def spotify_test(message):
    config = load_config(os.path.join('C2_Bot', 'mods', 'configs', 'spotify.toml'))
    print(config['spotify']['SPOTIPY_CLIENT_ID'])
    await


#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {'spotify_test' : spotify_test}
