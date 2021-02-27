import asyncio
import discord
import sqlite3

client = discord.Client()
conn = sqlite3.connect('c2_bot.db')
c = conn.cursor()

from C2_Bot.mods import *
from C2_Bot import __version__, discon, mod_list



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
        c.execute("ALTER TABLE maintbl ADD COLUMN {k} {v}".format(k=key, v=main_tbl_cols.get(key)))
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
    #run a command if prexix matches and 'command' after prefix is in client_functions
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
            elif c.execute('''SELECT EXISTS(SELECT 1 FROM funperm WHERE role_id={r}, guild_id={g}, fun={f})'''.format(r=message.author.id, g=message.guild.id, f=command)):
                try:
                    await client_functions[command](message = message)
                except Exception as e:
                    print(e)
            else:
                await message.channel.send('Insufficient Function Permissions')



async def mod_perm(message):
    '''explain function here'''
    mod_perm_raw = message.content.split()
    valid_role = False
    valid_fun = False
    c_new = []
    if len(mod_perm_raw) >= 3:
        guild_id, role_id, command = message.guild.id, mod_perm_raw[1], mod_perm_raw[2]
        if (target_role := discord.utils.find(lambda r: r.name == role_id, channel.guild.roles)) is not None:
            role_id, valid_role = target_role.id, True
        elif (target_role := discord.utils.find(lambda r: r.id == role_id, channel.guild.roles)) is not None:
            valid_role = True
        else:
            await message.channel.send('Invalid Role Input')
        for c in command:
            if c in client_functions:
                c_new.append(c)
                valid_fun = True
        command = c_new
        if len(command) == 0:
            await message.channel.send('Invalid Function Input')
        if valid_role and valid_fun:
            for c in command:
                if c.execute('''SELECT EXISTS(SELECT 1 FROM funperm WHERE role_id={r}, guild_id={g}, fun={f})'''.format(r=role_id, g=message.guild.id, f=c)):
                    c.execute('''DELETE FROM funperm WHERE (role_id={r}, guild_id={g}, fun={f})'''.format(r=role_id, g=message.guild.id, f=c))
                    conn.commit()
                else:
                    c.execute('''INSERT INTO funperm VALUES (role_id={r}, guild_id={g}, fun={f})'''.format(r=role_id, g=message.guild.id, f=c))
                    conn.commit()
            await message.channel.send('Permissions for {r} updated successfully!'.format(r=target_role.name))
    else:
        await message.channel.send('Insufficient mod_perm Parameters')




client.run(discon['secure']['TOKEN'])
