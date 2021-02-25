import asyncio
import discord
import sqlite3

client = discord.Client()
conn = sqlite3.connect('c2_bot.db')
c = conn.cursor()

from C2_Bot.mods import *
from C2_Bot import __version__, discon, mod_list



client_functions = {}
main_tbl_cols = {}
for sublibrary in mod_list:
    try:
        exec("from C2_Bot.mods.{s} import *".format(s=sublibrary))
        client_functions.update(client_fun)
        main_tbl_cols.update(main_tbl_col)
    except Exception as e:
        print(e)

#create function permission table if it does not exist
c.execute("CREATE TABLE IF NOT EXISTS funperm (role_id TEXT PRIMARY KEY, guild_id TEXT, fun TEXT)")
conn.commit()

#create main table if it does not exist
c.execute("CREATE TABLE IF NOT EXISTS maintbl (user_id TEXT PRIMARY KEY, guild_id TEXT)")
conn.commit()

#check main table and add missing columns
cols = c.execute("SELECT * FROM maintbl")
names = list(map(lambda x: x[0], cols.description))

for key in main_tbl_cols:
    if key not in names:
        c.execute("ALTER TABLE maintbl ADD COLUMN ? ?", (key, main_tbl_cols.get(key)))
        conn.commit()



def main():
    return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



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
                await message.channel.send('Insufficient Function Permissions')

client.run(discon['secure']['TOKEN'])
