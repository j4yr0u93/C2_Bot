import asyncio
import discord
import aiopolly


#config loading libs
import os.path
import qtoml as toml

def get_polly_client(path=os.path.join('C2_Bot', 'mods', 'configs', 'polly.toml')):
    with open(path, 'r') as f:
        config = toml.load(f)
    os.environ[''] = config['']['']
    polly_client =
    return polly_client

    async def tts_voice(client, msg, db, n):
        if not 1 <= n <= len(VOICES):
            raise CommandError(f'Voice ID must be between 1 and {len(VOICES)}.')
        cids, _ = db['tts'].get(msg.author.id, (set(), 'Joanna'))
        db['tts'][msg.author.id] = cids, VOICES[n-1]
        await reply_to(msg, f'Set your TTS voice to **{n}**.')
