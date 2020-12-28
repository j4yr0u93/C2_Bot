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
        if search_raw[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            search_limit = int(search_raw[2])
            search_query= " ".join(search_raw[3:])
        else:
            search_limit = 5
            search_query= " ".join(search_raw[2:])
    else:
        search_type = 'track'
        if search_raw[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            search_limit = int(search_raw[1])
            search_query= " ".join(search_raw[2:])
        else:
            search_limit = 5
            search_query= " ".join(search_raw[1:])
    search_results = spotify_client.search(search_query, type = search_type, limit=search_limit)
    search_result_urls = []
    for i in range(0, search_limit):
        search_result_urls.append(search_results['{st}s'.format(st=search_type)]['items'][i]['external_urls']['spotify'])
        urls = search_result_urls.join('\n')
    if search_limit > 1:
        await message.channel.send('{urls}\nThese are the top {sl} results for your {t} search: "{c}"'.format(urls=urls sl=search_limit, t=search_type, c=search_query))
    else:
        await message.channel.send(search_result_urls[0])

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'spotify_search' : spotify_search}
secure = {}
