import os
from dotenv import load_dotenv

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# load_dotenv() will look for '.env' file
load_dotenv()

# From .env file, get the variable named 'BOT_TOKEN'
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands
import scheduler
import users
import channels

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

# default
intents = discord.Intents.default()
intents.message_content = True

# https://stackoverflow.com/questions/73393567/discord-py-client-run-and-bot-run-in-one-code
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg):
    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    users_dict_temp = users.users_dict.copy()
    message = ''
    # Have to do this, else you get error channel has no attribute 'fetch_message'
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_check = await channel.fetch_message(arg)
    # Show ryuh-bot is typing...
    # 2 approaches:
    # a. ctx.typing()
    # b. message.channel.typing() <- this works both for 'ryuh check' n '!check <msg ID>' cmd
    async with message_to_check.channel.typing(): 
        for reaction in message_to_check.reactions:
            if(str(reaction) == "🐠"):
                message += "[Mon]\n"
                # message += mon_10_pm
                message += str(reaction)
            if(str(reaction) == "🐟"):
                # message += "mon "
                # message += mon_11_pm
                message += str(reaction)
            if(str(reaction) == "🐬"):
                message += "[Tue]\n"
                # message += tue_10_pm
                message += str(reaction)
            if(str(reaction) == "🐳"):
                # message += "tue "
                # message += tue_11_pm
                message += str(reaction)
            if(str(reaction) == "🐙"):
                message += "[Wed]\n"
                # message += wed_10_pm
                message += str(reaction)

            if(str(reaction) == "🐱"):
                message += "[Thu]\n"
                # message += thu_10_pm
                message += str(reaction)
            if(str(reaction) == "🐶"):
                # message += "thu"
                # message += thu_11_pm
                message += str(reaction)
            if(str(reaction) == "🐰"):
                message += "[Fri]\n"
                # message += fri_10_pm
                message += str(reaction)
            if(str(reaction) == "🐹"):
                # message += "fri"
                # message += fri_11_pm
                message += str(reaction)
            if(str(reaction) == "🐻"):
                # message += "fri"
                # message += fri_12_am
                message += str(reaction)
            if(str(reaction) == "🐯"):
                message += "[Sat]\n"
                # message += sat_10_pm
                message += str(reaction)
            if(str(reaction) == "🦁"):
                # message += "sat"
                # message += sat_11_pm
                message += str(reaction)
            if(str(reaction) == "🐼"):
                # message += "sat"
                # message += sat_12_am
                message += str(reaction)
            if(str(reaction) == "🐷"):
                message += "[Sun]\n"
                # message += sun_10_pm
                message += str(reaction)
            if(str(reaction) == "🐮"):
                # message += "sun"
                # message += sun_11_pm
                message += str(reaction)

            if(str(reaction) == "🙃"):
                message += "[Probably OT]\n"
                message += str(reaction)

            message += " : "
            async for user in reaction.users():
                if(str(user.id) in users.users_dict):
                    message += users.users_dict[str(user.id)]['emoji']
                # if is bot itself, dont add the blank emoji
                elif(user == client.user):
                    continue
                # you have to put str(), like str(user.id), else python will treat this if as true for all users
                if str(user.id) not in users_dict_temp:
                    continue
                users_dict_temp.pop(str(user.id))
            message += "\n"
        # if dict is empty
        if({} == users_dict_temp):
            message += 'everyone voted'
        else:
            for dis_tag, dis_info in users_dict_temp.items():
                for key in dis_info:
                    # print(dis_info)
                    if(key == 'name'):
                        # print(dis_info[key])
                        message += dis_info[key]
                        message += ', '
            # Remove last 2 char, because the msg will be "UserA, UserB, "
            message = message[:-2] + ' haven\'t vote'
    await message_to_check.reply(message)

@client.command()
async def delete(ctx, arg):
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_delete = await channel.fetch_message(arg)
    if(message_to_delete.author == client.user):
        await message_to_delete.delete()
    else:
        await ctx.channel.send("That message does not belong to me! I won't delete it.")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.lower() == 'ryuh bot':
        members = ''
        msg_sent = await message.channel.send(scheduler.schedule_message)
        msg_id = msg_sent.id
        if(message.channel.id == channels.js_hboss_channel_id):
            f = open("last_scheduled_msg_id_js.txt", "w")
        else:
            f = open("last_scheduled_msg_id_lz.txt", "w")
        f.write(str(msg_id))
        f.close()
        msg_to_react = await message.channel.fetch_message(msg_id)
        await msg_to_react.add_reaction("🐱")
        await msg_to_react.add_reaction("🐶")
        await msg_to_react.add_reaction("🐰")
        await msg_to_react.add_reaction("🐹")
        await msg_to_react.add_reaction("🐻")
        await msg_to_react.add_reaction("🐯")
        await msg_to_react.add_reaction("🦁")
        await msg_to_react.add_reaction("🐼")
        await msg_to_react.add_reaction("🐷")
        await msg_to_react.add_reaction("🐮")
        await msg_to_react.add_reaction("🐠")
        await msg_to_react.add_reaction("🐟")
        await msg_to_react.add_reaction("🐬")
        await msg_to_react.add_reaction("🐳")
        await msg_to_react.add_reaction("🐙")
        await msg_to_react.add_reaction("🙃")
        # dis_tag = 490507365704138763
        # dis_info = { 'name' : 'hwangz' , 'emoji' : '<:hwangz:1065984480860446781>'}
        for dis_tag, dis_info in users.users_dict.items():
            members += '<@'
            members += dis_tag # To append all mention ID into one single variable
            members += '> ' # add space
        # mention all at once
        await message.channel.send(members)

    if message.content.lower() == 'ryuh check':
        cur_ch_id = message.channel.id
        if(cur_ch_id == channels.js_hboss_channel_id):
            f = open("last_scheduled_msg_id_js.txt", "r")
        else:
            f = open("last_scheduled_msg_id_lz.txt", "r")
        last_scheduled_msg_id = f.read()
        f.close()
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
        await check(message, last_scheduled_msg_id)
    if message.author == client.user:
        return
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    await client.process_commands(message)


client.run(BOT_TOKEN)