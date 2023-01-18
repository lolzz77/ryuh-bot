import os
from dotenv import load_dotenv

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# load_dotenv() will look for '.env' file
load_dotenv()

# From .env file, get the variable named 'BOT_TOKEN'
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands
from datetime import date, timedelta, datetime
import pytz

# datetime.datetime.today().weekday()
# output:
# 0 = Monday
# 6 = Sunday
#
# date.today().strftime("%d/%b/%y")
# date format = dd/Jan/23
#
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

# not sure if this works, that is, i scare the .weekday() still uses default timezone
# this can be seen if you datetime.now(ytz.timezone('Asia/Singapore')).today()
# perhaps .today() is similar to .now() and it overwrites
my_timezone = pytz.timezone('Asia/Singapore')
now = datetime.now()
today_weekday = now.weekday()
first_day_of_week_offset = -today_weekday

monday = now + timedelta(days=first_day_of_week_offset+7)
monday = monday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

tuesday = now + timedelta(days=first_day_of_week_offset+7)
tuesday = tuesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

wednesday = now + timedelta(days=first_day_of_week_offset+7)
wednesday = wednesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

thursday = now + timedelta(days=first_day_of_week_offset)
thursday = thursday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

friday = now + timedelta(days=first_day_of_week_offset)
friday = friday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

saturday = now + timedelta(days=first_day_of_week_offset)
saturday = saturday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

sunday = now + timedelta(days=first_day_of_week_offset)
sunday = sunday.strftime("%d/%b/%y")

schedule_weekend_msg = '''\
Thursday Night - **{thursday}**

10pm - 🐱 
11pm - 🐶 

Friday Night - **{friday}**

10pm - 🐰 
11pm - 🐹 
12am - 🐻 

Saturday Night - **{saturday}**

10pm - 🐯 
11pm - 🦁 
12am - 🐼

Sunday Night - **{sunday}**

10pm - 🐷
11pm - 🐮
all cannot - 🙃\
'''.format(thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)

schedule_weekday_msg = '''\
Monday Night - **{monday}**

10pm - 🐠
11pm - 🐟

Tuesday Night - **{tuesday}**

10pm - 🐬
11pm - 🐳

Wednesday Night - **{wednesday}**

10pm - 🐙

all cannot - 🙃\
'''.format(monday=monday, tuesday=tuesday, wednesday=wednesday)

# default
intents = discord.Intents.default()
intents.message_content = True


# Jumping Sushi hboss-sellherbs channel
channel_id = 963160372385296414

# my #general channel
# channel_id = 803958155935219724

# This is nested dictionary
users_dict = {
    'hwangz#8075'           : { 'name' : 'hwangz' , 'id' : '<@490507365704138763>' },
    'Fruit#8143'            : { 'name' : 'kong'   , 'id' : '<@274075256275206145>' },
    'FloatLikeBubble#0529'  : { 'name' : 'tele'   , 'id' : '<@311477931576918016>' },
    'Jasmine#4582'          : { 'name' : 'jazz'   , 'id' : '<@389193536043483138>' },
    'LL#2409'               : { 'name' : 'ryuh'   , 'id' : '<@702529999068200970>' },
    'kevinc#3600'           : { 'name' : 'kevin'  , 'id' : '<@131389918998953985>' },
    # 'clem#1138'             : { 'name' : 'clem'   , 'id' : '<@304579645003530251>' },
}

# https://stackoverflow.com/questions/73393567/discord-py-client-run-and-bot-run-in-one-code
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg):
    message = ''
    channel = client.get_channel(channel_id)
    message_to_check = await channel.fetch_message(arg)
    for reaction in message_to_check.reactions:
        async for user in reaction.users():
            if(None == users_dict[str(user)]):
                continue
            users_dict.pop(str(user))
    # if dict is empty
    if({} == users_dict):
        message = 'everyone voted'
    else:
        for dis_tag, dis_info in users_dict.items():
            for key in dis_info:
                # print(dis_info)
                if(key == 'name'):
                    # print(dis_info[key])
                    message += dis_info[key]
                    message += ', '
        message = message[:-2] + ' not yet vote'
    await ctx.send(message)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('ryuh weekend'):
        members = ''
        msg_sent = await message.channel.send(schedule_weekend_msg)
        msg_id = msg_sent.id
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
        await msg_to_react.add_reaction("🙃")
        for dis_tag, dis_info in users_dict.items():
            for key in dis_info:
                if(key == 'id'):
                    members += dis_info[key] # To append all mention ID into one single variable
                    members += ' ' # add space
        # mention all at once
        await message.channel.send(members)

    if message.content.startswith('ryuh weekday'):
        members = ''
        msg_sent = await message.channel.send(schedule_weekday_msg)
        msg_id = msg_sent.id
        msg_to_react = await message.channel.fetch_message(msg_id)
        await msg_to_react.add_reaction("🐠")
        await msg_to_react.add_reaction("🐟")
        await msg_to_react.add_reaction("🐬")
        await msg_to_react.add_reaction("🐳")
        await msg_to_react.add_reaction("🐙")
        await msg_to_react.add_reaction("🙃")
        for dis_tag, dis_info in users_dict.items():
            for key in dis_info:
                if(key == 'id'):
                    members += dis_info[key]
                    members += ' '
        await message.channel.send(members)

    if message.author == client.user:
        return
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    await client.process_commands(message)


client.run(BOT_TOKEN)