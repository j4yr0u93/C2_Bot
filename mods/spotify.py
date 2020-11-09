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
    '''Passes literal input to spotify.search() function'''
    search_raw = message.content.split()
    search_query = " ".join(search_raw[1:])
    search_results = spotify_client.search(search_query)
#    result_url = search_results.get('external_urls')
    await message.channel.send(search_results)

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}
