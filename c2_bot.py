import asyncio
import discord
import sqlite3

client = discord.Client()
conn = sqlite3.connect('c2_bot.db')
c = conn.cursor()

from C2_Bot.mods import *
from C2_Bot import __version__, discon, mod_list



client_functions = {}
for sublibrary in mod_list:
    try:
        exec("from C2_Bot.mods.{s} import *".format(s=sublibrary))
        client_functions.update(client_fun)
    except Exception as e:
        print(e)

def main():
    return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client_functions)



#message user welcome message when they join server
#@client.event
#async def on_member_join(member):
#    if member.guild.system_channel != None:
#        await member.guild.system_channel.send(f'{member.mention}')


@client.event
async def on_message(message):
    #ignore bots
    if message.author.bot:
        return
    #run a command if prexix matches and first 'word' after prefixes is in 'commands'
    elif message.content.startswith(discon['options']['PREFIX']):
        command_string = message.content
        command_parse = command_string.split()
        command = command_parse[0][len(discon['options']['PREFIX']):]
        if command in client_functions:
            if (message.author.id == message.guild.owner.id) or message.author.guild_permissions.administrator:
                try:
                    await client_functions[command](message = message)
                except Exception as e:
                    print(e)
            else:
                await message.channel.send('You do not have permission to use this function!')

client.run(discon['secure']['TOKEN'])
