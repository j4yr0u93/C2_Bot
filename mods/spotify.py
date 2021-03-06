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
    '''Spotify searching function that returns the first n spotify urls for a search type'''
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
    results = search_results[f'{search_type}s']['items']
    urls = "\n".join(results[i]['external_urls']['spotify'] for i in range(search_limit))
    if search_limit > 1:
        await message.channel.send('{urls}\nThese are the top {sl} results for your {t} search: "{c}"'.format(urls=urls, sl=search_limit, t=search_type, c=search_query))
    else:
        await message.channel.send(urls)

async def related(message, spotify_client = get_spotify_client()):
    search_raw = message.content.split()
    artist_data = spotify_client.search(' '.join(search_raw[1:]), type = 'artist', limit=1)
    artist_url = artist_data['artists']['items'][0]['external_urls']['spotify']
    related_data = spotify_client.artist_related_artists(artist_url)
    await print(related_data)

#async def song_rec(message, spotify_client = get_spotify_client()):
#    '''Spotify song recommendation function that takes a song URL and returns recommendations'''
#    search_raw = message.content.split()
#    print(search_raw[2])
#    track_recs = spotify_client.recommendations(seed_tracks=search_raw[2], limit=search_raw[1])
#    await print(track_recs)

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
client_fun = {'spotify_search' : spotify_search, 'related' : related}

main_tbl_col = {'favorite_track' : 'TEXT'}
