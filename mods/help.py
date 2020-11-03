import asyncio
import discord

async def test(message):
    await message.channel.send('Nice test!')

async def echo(message):
    echo_raw = message.content.split()
    echo_content = " ".join(echo_raw[1:])
    await message.channel.send(echo_content)

async def author_id(message):
    await message.channel.send(message.author.id())

async def monke(message):
    await message.channel.send('dev who made bot is monke')


allowed = {'test' : test, 'echo' : echo, 'author_id' : author_id}
secure = {'monke' : monke}
