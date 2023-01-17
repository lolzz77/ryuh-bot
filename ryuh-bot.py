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

# https://stackoverflow.com/questions/73393567/discord-py-client-run-and-bot-run-in-one-code
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg):
    message = ''
    users_dict = {
        'hwangz#8075'           :'hwangz',
        'Fruit#8143'            :'kong',
        'FloatLikeBubble#0529'  :'tele',
        'Jasmine#4582'          :'jazz',
        'clem#1138'             :'clem',
        'LL#2409'               :'ryuh',
        'kevinc#3600'           :'kevin',
    }
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
        for k in list(users_dict.values()):
            message += k
            message += ', '
        message = message[:-2] + ' not yet vote'
    await ctx.send(message)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global is_weekend
    if message.content.startswith('ryuh weekend'):
        is_weekend = True
        await message.channel.send(schedule_weekend_msg)
    if message.content.startswith('ryuh weekday'):
        is_weekend = False
        await message.channel.send(schedule_weekday_msg)
    if message.author == client.user:
        if is_weekend:
            await message.add_reaction("🐱")
            await message.add_reaction("🐶")
            await message.add_reaction("🐰")
            await message.add_reaction("🐹")
            await message.add_reaction("🐻")
            await message.add_reaction("🐯")
            await message.add_reaction("🦁")
            await message.add_reaction("🐼")
            await message.add_reaction("🐷")
            await message.add_reaction("🐮")
            await message.add_reaction("🙃")
        else:
            await message.add_reaction("🐠")
            await message.add_reaction("🐟")
            await message.add_reaction("🐬")
            await message.add_reaction("🐳")
            await message.add_reaction("🐙")
            await message.add_reaction("🙃")
    # https://stackoverflow.com/questions/65207823/discord-py-bot-command-not-running
    await client.process_commands(message)


client.run(BOT_TOKEN)