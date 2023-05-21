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
    bossing_day_message = []
    bossing_day = ''
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
                bossing_day = scheduler.result_monday_10pm
                message += str(reaction)
            if(str(reaction) == "🐟"):
                message += str(reaction)
                bossing_day = scheduler.result_monday_11pm
            if(str(reaction) == "🐬"):
                message += "[Tue]\n"
                message += str(reaction)
                bossing_day = scheduler.result_tuesday_10pm
            if(str(reaction) == "🐳"):
                message += str(reaction)
                bossing_day = scheduler.result_tuesday_11pm
            if(str(reaction) == "🐙"):
                message += "[Wed]\n"
                message += str(reaction)
                bossing_day = scheduler.result_wednesday_10pm

            if(str(reaction) == "🐱"):
                message += "[Curse]\n"
                message += str(reaction)
                bossing_day = scheduler.result_thursday_10pm
            if(str(reaction) == "🐶"):
                message += str(reaction)
                bossing_day = scheduler.result_thursday_11pm
            if(str(reaction) == "🐰"):
                message += "[Fri]\n"
                message += str(reaction)
                bossing_day = scheduler.result_friday_10pm
            if(str(reaction) == "🐹"):
                message += str(reaction)
                bossing_day = scheduler.result_friday_11pm
            if(str(reaction) == "🐻"):
                message += str(reaction)
                bossing_day = scheduler.result_friday_12am
            if(str(reaction) == "🐯"):
                message += "[Sat]\n"
                message += str(reaction)
                bossing_day = scheduler.result_saturday_10pm
            if(str(reaction) == "🦁"):
                message += str(reaction)
                bossing_day = scheduler.result_saturday_11pm
            if(str(reaction) == "🐼"):
                message += str(reaction)
                bossing_day = scheduler.result_saturday_12am
            if(str(reaction) == "🐷"):
                message += "[Sun]\n"
                message += str(reaction)
                bossing_day = scheduler.result_sunday_10pm
            if(str(reaction) == "🐮"):
                message += str(reaction)
                bossing_day = scheduler.result_sunday_11pm

            # if(str(reaction) == "🐠"):
            #     message += "[Mon]\n"
            #     bossing_day = 'Monday 10pm!'
            #     message += str(reaction)
            # if(str(reaction) == "🐟"):
            #     message += str(reaction)
            #     bossing_day = 'Monday 11pm!'
            # if(str(reaction) == "🐬"):
            #     message += "[Tue]\n"
            #     message += str(reaction)
            #     bossing_day = 'Tuesday 10pm!'
            # if(str(reaction) == "🐳"):
            #     message += str(reaction)
            #     bossing_day = 'Tuesday 11pm!'
            # if(str(reaction) == "🐙"):
            #     message += "[Wed]\n"
            #     message += str(reaction)
            #     bossing_day = 'Wednesday 10pm!'

            # if(str(reaction) == "🐱"):
            #     message += "[Thu]\n"
            #     message += str(reaction)
            #     bossing_day = 'Thursday 10pm!'
            # if(str(reaction) == "🐶"):
            #     message += str(reaction)
            #     bossing_day = 'Thursday 11pm!'
            # if(str(reaction) == "🐰"):
            #     message += "[Fri]\n"
            #     message += str(reaction)
            #     bossing_day = 'Friday 10pm!'
            # if(str(reaction) == "🐹"):
            #     message += str(reaction)
            #     bossing_day = 'Friday 11pm!'
            # if(str(reaction) == "🐻"):
            #     message += str(reaction)
            #     bossing_day = 'Friday 12am!'
            # if(str(reaction) == "<:pepe_birthday:1087764773615194212>"):
            #     message += "[Sat]\n"
            #     message += str(reaction)
            #     bossing_day = 'Saturday 10pm!'
            # if(str(reaction) == "🍰"):
            #     message += str(reaction)
            #     bossing_day = 'Saturday 11pm!'
            # if(str(reaction) == "<a:cake2:1087764775754280961>"):
            #     message += str(reaction)
            #     bossing_day = 'Saturday 12am!'
            # if(str(reaction) == "🎂"):
            #     message += "[Sun]\n"
            #     message += str(reaction)
            #     bossing_day = 'Sunday 10pm!'
            # if(str(reaction) == "<a:cake1:1087763631346810912>"):
            #     message += str(reaction)
            #     bossing_day = 'Sunday 11pm!'

            if(str(reaction) == "🙃"):
                message += "[Probably OT]\n"
                message += str(reaction)

            message += " : "
            count = 0
            async for user in reaction.users():
                if(str(user.id) in users.users_dict):
                    message += users.users_dict[str(user.id)]['emoji']
                    count += 1
                # if is bot itself, dont add the blank emoji
                elif(user == client.user):
                    continue
                # you have to put str(), like str(user.id), else python will treat this if as true for all users
                if str(user.id) not in users_dict_temp:
                    continue
                users_dict_temp.pop(str(user.id))
            message += "\n"
            if count == 6:
                bossing_day_message.append(bossing_day)
        # if dict is empty
        if({} == users_dict_temp):
            message += 'everyone voted'
            message += '\n'
            if not bossing_day_message:
                message += "there's no consensus on the bossing date"
            else:
                for day in bossing_day_message:
                    message += day
                    message += '\n'
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

@client.command()
async def test(ctx):
    # get emoji id by running '\:name:'
    js_bossing_channel = 963160372385296414
    # my_discord_general_channel = 803958155935219724
    channel = client.get_channel(js_bossing_channel)
    # guild = 491039338659053568
    # emoji = discord.utils.get(ctx.guild.emojis, id=811260045307543553)
    # emoji = discord.utils.get(client.emojis, name='Birthday_Cake')
    # await channel.send("<a:Birthday_Cake:811260045307543553>")
    # emoji = client.get_emoji(811260045307543553)
    # await channel.send(emoji)
    await channel.send("<:thumbsupright:1079644743107092511>")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.lower() == 'ryuh bot':
        # Send schedule message to channel
        msg_sent = await message.channel.send(scheduler.schedule_message)

        # Get the schedule msg ID sent by bot, to save in file, for 'ryuh check' command to retrieve
        msg_id = msg_sent.id 

        file_path = scheduler.SCHEDULE_PATH + str(message.channel.id) + '.txt'
        
        # Check if file exists
        isExist = os.path.exists(file_path)

        # If not, create it
        if(False == isExist):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        f = open(file_path, "w")
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

        # await msg_to_react.add_reaction("🐱")
        # await msg_to_react.add_reaction("🐶")
        # await msg_to_react.add_reaction("🐰")
        # await msg_to_react.add_reaction("🐹")
        # await msg_to_react.add_reaction("🐻")
        # await msg_to_react.add_reaction("<:pepe_birthday:1087764773615194212>")
        # await msg_to_react.add_reaction("🍰")
        # await msg_to_react.add_reaction("<a:cake2:1087764775754280961>")
        # await msg_to_react.add_reaction("🎂")
        # await msg_to_react.add_reaction("<a:cake1:1087763631346810912>")
        # await msg_to_react.add_reaction("🐠")
        # await msg_to_react.add_reaction("🐟")
        # await msg_to_react.add_reaction("🐬")
        # await msg_to_react.add_reaction("🐳")
        # await msg_to_react.add_reaction("🐙")
        # await msg_to_react.add_reaction("🙃")

        # Mention by role, have to have '&' for role mentions
        mention = '<@&' + str(users.party_role_id) + '>'
        await message.channel.send(mention)

    if message.content.lower() == 'ryuh weekday' or message.content.lower() == 'ryuh weekend':
        # Send schedule message to channel
        msg_sent = await message.channel.send("This command is deprecated. Please use 'ryuh bot' instead.")

    if message.content.lower() == 'ryuh check':
        file_path = scheduler.SCHEDULE_PATH + str(message.channel.id) + '.txt'
        f = open(file_path, "r")
        msg_id = f.read()
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
        await check(message, msg_id)
    if message.author == client.user:
        return
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    await client.process_commands(message)


client.run(BOT_TOKEN)