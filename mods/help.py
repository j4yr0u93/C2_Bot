import asyncio
import discord

async def test(message):
    await message.channel.send('Nice test!')

async def echo(message):
    echo_raw = message.content.split()
    echo_content = " ".join(echo_raw[1:])
    await message.channel.send()

async def monke(message):
    await message.channel.send('dev who made bot is monke')


allowed = {'test' : test, 'echo' : echo}
secure = {'monke' : monke}
