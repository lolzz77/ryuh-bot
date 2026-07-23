import os
from dotenv import load_dotenv
from discord.ext import commands
import emojis as emoji_v2
import inspect

from module import testData
from module import error
from module import config
from module import scheduler
from module import utils
from module import client
from module import version

THIS_FILENAME = os.path.basename(inspect.getfile(inspect.currentframe()))
version = version.version
print(f"Version: {version}")

# Read .env file
load_dotenv()
# From .env file, get the BOT_TOKEN value
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print(f"BOT TOKEN is null")
    exit()

intents = client.intents
client = client.client

@client.event
async def on_ready():
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(f"{THIS_FILENAME}:{str(inspect.currentframe().f_code.co_name)}:{str(inspect.currentframe().f_lineno)}")
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(f"{THIS_FILENAME}:{str(inspect.currentframe().f_code.co_name)}:{str(inspect.currentframe().f_lineno)}")

    # Channel that has the message for a list of users
    users_channel_id = 0
    # Channel that has the message for schedule template
    schedule_channel_id = 0

    if message.guild.id == testData.my_discord:
        users_channel_id = testData.my_discord_ryuh_bot_channel_user
        schedule_channel_id = testData.my_discord_ryuh_bot_channel_schedule
    elif message.guild.id == testData.js_discord:
        users_channel_id = testData.js_bossing_channel_user
        schedule_channel_id = testData.js_bossing_channel_schedule

    if message.content.lower() == 'ryuh bot':
        """
        Post the schedule template
        """
        utils.check_json_exists(message.channel.id)

        mention = ''
        # Fetch required data from discord chat
        try:
            schedule_message, emoji_list_decoded = await utils.read_schedule(schedule_channel_id, message.channel.id)
        except Exception as exception_error:
            error.error_message = str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno) + ':Error'
            await message.channel.send(error.error_message)
            await message.channel.send(exception_error)
            return

        if not schedule_message or not emoji_list_decoded:
            await message.channel.send(error.error_message)
            return

        users_dict = await utils.read_user(users_channel_id)
        if not users_dict:
            await message.channel.send(error.error_message)
            return

        # Send schedule message to channel
        msg_sent = await message.channel.send(schedule_message)
        msg_id = msg_sent.id

        file_path = utils.check_json_exists(message.channel.id)
        json_data = utils.read_file(file_path)
        json_data["schedule"] = msg_id
        utils.write_file(json_data, file_path)

        # Now react all the emojis on the schedule template the bot sent
        msg_to_react = await message.channel.fetch_message(msg_id)

        # react on the message
        for e in emoji_list_decoded:
            await msg_to_react.add_reaction(emoji_v2.encode(e))

        # ping those affected users
        # If want mention by role, have to have '&' for role mentions
        # eg: '<@&[role_id]>'
        for user in users_dict:
            mention += '<@' + str(user) + '> '
        await message.channel.send(mention)

    if message.content.lower() == 'chagee':
        msg_sent = await message.channel.send("thanks")

    if message.content.lower() == 'ryuh check':
        file_path = utils.check_json_exists(message.channel.id)
        json_data = utils.read_file(file_path)
        msg_id = json_data["schedule"]

        await utils.check(message, msg_id, users_channel_id, schedule_channel_id)

    if message.content.lower() == 'wingardium leviosa':
        file_path = utils.check_json_exists(message.channel.id)
        json_data = utils.read_file(file_path)
        json_data["black_mage_done"] = "1"
        utils.write_file(json_data, file_path)
        await message.channel.send(f"Black Mage {json_data["black_mage_month"]} marked done")

    if message.content.lower() == 'expecto patronum':
        file_path = utils.check_json_exists(message.channel.id)
        json_data = utils.read_file(file_path)
        json_data["black_mage_done"] = "0"
        utils.write_file(json_data, file_path)
        await message.channel.send(f"Black Mage {json_data["black_mage_month"]} marked NOT done")

    # If ping bot, get the last `ryuh check` message
    if str(client.user.id) in message.content:
        file_path = utils.check_json_exists(message.channel.id)
        json_data = utils.read_file(file_path)
        msg_id = json_data["schedule_check_result"]
        message_to_write = '.'
        channel = client.get_channel(message.channel.id)
        message_to_reply = await channel.fetch_message(msg_id)
        await message_to_reply.reply(message_to_write)

    # If message is sent by bot, do nothing
    if message.author == client.user:
        return

    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    # This line is necessary to run '@client.command()' functions
    await client.process_commands(message)


client.run(BOT_TOKEN)