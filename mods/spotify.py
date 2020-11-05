import asyncio
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#init
import os.path
import qtoml as toml

#open config with right path
SPOTIFY_CONFIG_PATH = os.path.join('C2_Bot', 'mods', 'configs', 'spotify.toml')

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
        return config

def set_spot_env(config):
    os.environ['SPOTIPY_CLIENT_ID'] = spotify['spotify']['SPOTIPY_CLIENT_ID']
    os.environ['SPOTIPY_CLIENT_SECRET'] = spotify['spotify']['SPOTIPY_CLIENT_SECRET']
    os.environ['SPOTIPY_REDIRECT_URI'] = spotify['spotify']['SPOTIPY_REDIRECT_URI']
    return

#load auth
set_spot_env(load_config(CONFIG_PATH))

#set auth
spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

async def spotify_search(message):
    '''Passes literal input to spotify.search() function'''
    search_raw = message.content.split()
    search_query = " ".join(echo_raw[1:])
    search_results = spotify.search(search_query)
    result_url = search_results.get('external_urls').get('spotify')
    await message.channel.send(result_url)

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}