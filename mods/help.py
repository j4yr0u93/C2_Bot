import asyncio
import discord

async def test(message):
    await message.channel.send('Nice test!')

async def echo(message):
    await message.channel.send(str())

async def monke(message):
    await message.channel.send('dev who made bot is monke')


allowed = {'test' : test, 'echo' : echo}
secure = {'monke' : monke}
