import sys
import os
from dotenv import load_dotenv
from discord.ext import commands
from module import testData
from module import error
import inspect
from module import config

# To import python from other directory, you can do in 2 ways:
# way 1:
# import sys
# sys.path.append("module")
#
# this method is dangerous
# when run in vs code or in command line 'python3 main.py'
# it will have no problem
# however, this got problem when you build executable
# it will compain cannot find module 'pytz' and other modules
# because you modified the path to have 'module' in the path
# if you do this, you have to copy 'module' folder into where .exe is located
# then, copy 'pytz' module into this 'module' folder as well

# way 2:
# from 'path to include' import 'file name'
from module import scheduler
from module import utils
from module import client
from module import version

version = version.version
print("Version: " + version)

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# load_dotenv() will look for '.env' file
load_dotenv()

# From .env file, get the variable named 'BOT_TOKEN'
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("BOT TOKEN is null")
    exit()

# if you get error 
# 'NoneType' object has no attribute 'fetch_message'
# code example:
# channel = client.get_channel(803958155935219724)
# msg = await channel.fetch_message(1062756653054824478)
# This means channel is NULL
# it cannot find 'channel' you specified.
# to solve this you have to put them under on_ready() function
# Stackoverflow: It seems like you are trying to call a bot's functionality before actually running your bot.
# Try to add your code inside on_ready() callback to ensure that you are trying to get your channel only after initializing the bot itself.

intents = client.intents
client = client.client

@client.event
async def on_ready():
    # this prints current file path : current function : current line
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # Get channel name and ID
    # output: my discord general channel, the output will be 'general'
    channel_name = message.channel.name
    # output: 803958155935219724
    channel_id = message.channel.id
    # print(channel_name)
    # print(channel_id)
    users_channel_id = 0
    schedule_channel_id = 0

    if message.guild.id == testData.my_discord:
        users_channel_id = testData.my_discord_ryuh_bot_channel_user
        schedule_channel_id = testData.my_discord_ryuh_bot_channel_schedule
    elif message.guild.id == testData.js_discord:
        users_channel_id = testData.js_bossing_channel_user
        schedule_channel_id = testData.js_bossing_channel_schedule

    if message.content.lower() == 'ryuh bot':
        mention = ''
        
        # Fetch required data from discord chat
        try:
            schedule_message, emoji_list = await utils.read_schedule(schedule_channel_id)
        except Exception as exception_error:
            error.error_message = str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno) + ':Error'
            await message.channel.send(error.error_message)
            await message.channel.send(exception_error)
            return

        if not schedule_message or not emoji_list:
            await message.channel.send(error.error_message)
            return

        users_dict = await utils.read_user(users_channel_id)
        if not users_dict:
            await message.channel.send(error.error_message)
            return

        # Send schedule message to channel
        msg_sent = await message.channel.send(schedule_message)

        # write the sent message ID into a file, to retrieve for 'checking' feature
        msg_id = utils.write_file(message, msg_sent)

        # get the sent message ID
        msg_to_react = await message.channel.fetch_message(msg_id)

        # react on the message
        for e in emoji_list:
            await msg_to_react.add_reaction(e)

        # ping those affected users
        # If want mention by role, have to have '&' for role mentions
        # eg: '<@&[role_id]>'
        for user in users_dict:
            mention += '<@' + str(user) + '> '
        await message.channel.send(mention)

    if message.content.lower() == 'ryuh weekday' or message.content.lower() == 'ryuh weekend':
        # Send schedule message to channel
        msg_sent = await message.channel.send("This command is deprecated. Please use 'ryuh bot' instead.")

    if message.content.lower() == 'chagee':
        msg_sent = await message.channel.send("thanks")

    if message.content.lower() == 'checkgee':
        msg_sent = await message.channel.send("u mean chagee?")

    if message.content.lower() == 'ryuh check':
        msg_id = utils.read_file(message)

        # if you want bot to execute bot command
        # e.g.: bot to call "!check [msg_id]"
        # you dont need to, u just need to call the function
        # as for funciton 1st param "ctx", just pass you have to pass message.channel
        # because in the function, there's "ctx.send()"
        # and only "message.channel" has ".send()" method
        # UPDATE 1: now you want to use "reply()"
        # Then pass only "message"
        # "message.channel" -> has method ".send()
        # "message" -> has method .reply()
        # UPDATE 2: Since you want bot to reply to specific msg ID
        # then you dont need to pass anything for 1st param, just pass None
        await utils.check(message, msg_id, users_channel_id, schedule_channel_id)

    # If message is sent by bot, do nothing
    if message.author == client.user:
        return
    
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    # This line is necessary to run '@client.command()' functions
    await client.process_commands(message)


client.run(BOT_TOKEN)