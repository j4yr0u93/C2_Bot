import asyncio
import discord

#async def help(message):
#    if message.content()[-4:] == 'help':
#        af = allowed_functions.keys().join()
#        'Available functions are: {af}'.format(af = af)

async def test(message):
    '''This function outputs a string to confirm that seamless module integration is functioning'''
    await message.channel.send('Nice test!')

async def echo(message):
    '''This function reiterates whatever string input is read in'''
    echo_raw = message.content.split()
    echo_content = " ".join(echo_raw[1:])
    await message.channel.send(echo_content)

async def secure_test(message):
    '''This function is to confirm that only permitted users can run secure functions'''
    await message.channel.send('Successful secure test')

#these dictionaries indicate which user level can run which functions, everyone or the designated secure roles
allowed = {'test' : test, 'echo' : echo}
secure = {'secure_test' : secure_test}
