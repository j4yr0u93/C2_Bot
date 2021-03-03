import asyncio
import discord
import sqlite3

client = discord.Client()
conn = sqlite3.connect('c2_bot.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

from C2_Bot.mods import *
from C2_Bot import __version__, discon, mod_list



#message user welcome message when they join server
#@client.event
#async def on_member_join(member):
#    if member.guild.system_channel != None:
#        await member.guild.system_channel.send(f'{member.mention}')


def main():
    return

@client.event
async def on_message(message):
    #ignore bots
    if message.author.bot:
        return
    #run a command if prexix matches and 'command' after prefix is in client_functions
    elif message.content.startswith(discon['options']['PREFIX']):
        command_string = message.content
        command_parse = command_string.split()
        command = command_parse[0][len(discon['options']['PREFIX']):]
        if command in client_functions:
            if message.author.guild_permissions.administrator:
                try:
                    await client_functions[command](message = message)
                except Exception as e:
                    print(e)
            elif any([command in c.execute("SELECT fun FROM funperm WHERE role_id='{r}' AND guild_id='{g}'".format(r=role.id, g=message.guild.id)).fetchall() for role in message.author.roles]):
                try:
                    await client_functions[command](message = message)
                except Exception as e:
                    print(e)
            else:
                await message.channel.send('Insufficient Function Permissions')



async def mod_perm(message):
    mod_perm_raw = message.content.split()
    valid_role = False
    valid_fun = False
    c_new = []
    if len(mod_perm_raw) >= 3:
        guild_id, role_id, command = message.guild.id, mod_perm_raw[1], list(mod_perm_raw[2:])
        if (target_role := discord.utils.find(lambda r: r.name == role_id, message.channel.guild.roles)) is not None:
            role_id, valid_role = target_role.id, True
        elif (target_role := discord.utils.find(lambda r: r.id == role_id, message.channel.guild.roles)) is not None:
            valid_role = True
        else:
            await message.channel.send('Invalid Role Input')
        for i in range(len(command)):
            if command[i-1] in client_functions:
                c_new.append(command[i-1])
                valid_fun = True
        command = c_new
        if len(command) == 0:
            await message.channel.send('Invalid Function Input')
        if valid_role and valid_fun:
            for i in range(len(command)):
                if command[i-1] in c.execute("SELECT fun FROM funperm WHERE role_id='{r}' AND guild_id='{g}'".format(r=role_id, g=message.guild.id)).fetchall():
                    try:
                        c.execute("DELETE FROM funperm WHERE role_id='{r}' AND guild_id='{g}' AND fun='{f}'".format(r=role_id, g=message.guild.id, f=command[i-1]))
                        conn.commit()
                    except Exception as e:
                        print(e)
                else:
                    try:
                        c.execute("INSERT INTO funperm (role_id, guild_id, fun) VALUES ('{r}', '{g}', '{f}')".format(r=role_id, g=message.guild.id, f=command[i-1]))
                        conn.commit()
                    except Exception as e:
                        print(e)
            await message.channel.send('Permissions for {r} updated successfully!'.format(r=target_role.name))
    else:
        await message.channel.send('Insufficient mod_perm Parameters')


client_functions = {'mod_perm' : mod_perm}
main_tbl_cols = {}
for sublibrary in mod_list:
    try:
        exec("from C2_Bot.mods.{s} import *".format(s=sublibrary))
        client_functions.update(client_fun)
        main_tbl_cols.update(main_tbl_col)
    except Exception as e:
        print(e)

#create function permission table if it does not exist
c.execute("CREATE TABLE IF NOT EXISTS funperm (role_id TEXT, guild_id TEXT, fun TEXT)")
conn.commit()

#create main table if it does not exist
c.execute("CREATE TABLE IF NOT EXISTS maintbl (user_id TEXT, guild_id TEXT)")
conn.commit()

#check main table and add missing columns
cols = c.execute("SELECT * FROM maintbl")
names = list(map(lambda x: x[0], cols.description))

for key in main_tbl_cols:
    if key not in names:
        c.execute("ALTER TABLE maintbl ADD COLUMN {k} {v}".format(k=key, v=main_tbl_cols.get(key)))
        conn.commit()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.run(discon['secure']['TOKEN'])
