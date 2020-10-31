import asyncio
import discord

from C2_Bot import __version__, discon

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#message user welcome message when they join server
@client.event
async def on_member_join(member):
    if member.guild.id == discon['id']['SERVER']:
        channel = client.get_channel(discon['id']['WELCOME'])
        await channel.send(f'{member.mention}')


@client.event
async def on_message(message):
    #ignore bots
    if message.author.bot:
        return

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(discon['secure']['TOKEN'])
