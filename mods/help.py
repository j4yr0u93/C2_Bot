import asyncio
import discord

allowed_functions = {'test' : test, 'echo' : echo}

secure_functions = {'monke' : monke}

async def test(message):
    await message.channel.send('Nice test!')

async def echo(message):
    await message.channel.send(str())

async def monke(message):
    await message.channel.send('dev who made bot is monke')
