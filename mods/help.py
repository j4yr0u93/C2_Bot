import asyncio
import discord

allowed_functions = ['test', 'echo']

async def test(args, message):
    await message.channel.send('Nice test!')

async def echo(args, message):
    await message.channel.send(str(args))
