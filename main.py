import os
from dotenv import load_dotenv

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# load_dotenv() will look for '.env' file
load_dotenv()

# From .env file, get the variable named 'BOT_TOKEN'
BOT_TOKEN = os.getenv('BOT_TOKEN')

from discord.ext import commands
import scheduler
import users
import utils
import client

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
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.lower() == 'ryuh bot':
        # Send schedule message to channel
        msg_sent = await message.channel.send(scheduler.schedule_message)

        msg_id = utils.write_file(message, msg_sent)

        msg_to_react = await message.channel.fetch_message(msg_id)
        for e in scheduler.reaction_mapping:
            await msg_to_react.add_reaction(e)
            
        # Mention by role, have to have '&' for role mentions
        mention = '<@&' + str(users.party_role_id) + '>'
        await message.channel.send(mention)

    if message.content.lower() == 'ryuh weekday' or message.content.lower() == 'ryuh weekend':
        # Send schedule message to channel
        msg_sent = await message.channel.send("This command is deprecated. Please use 'ryuh bot' instead.")

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
        await utils.check(message, msg_id)

    # If message is sent by bot, do nothing
    if message.author == client.user:
        return
    
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    # This line is necessary to run '@client.command()' functions
    await client.process_commands(message)


client.run(BOT_TOKEN)