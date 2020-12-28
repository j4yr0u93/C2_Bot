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
    '''Spotify searching function that returns the first spotify url for a search'''
    search_raw = message.content.split()
    search_type = search_raw[1]
    search_query= " ".join(search_raw[2:])
    search_results = spotify_client.search(search_query, type = search_type, limit=5)
    for i in range(0, 5):
        search_result_url = search_results['tracks']['items'][i]['external_urls']['spotify']
        await message.channel.send(search_result_url)
    await message.channel.send('These are the top 5 results for your {t} search'.format(t=search_type))

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}
