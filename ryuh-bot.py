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
js_hboss_channel_id = 963160372385296414

# my #general channel
my_gen_channel_id = 803958155935219724

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
    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    users_dict_temp = users_dict.copy()
    message = ''
    # Have to do this, else you get error channel has no attribute 'fetch_message'
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_check = await channel.fetch_message(arg)
    for reaction in message_to_check.reactions:
        async for user in reaction.users():
            # you have to str(user) else python will treat this if as true for all users
            if str(user) not in users_dict_temp:
                continue
            users_dict_temp.pop(str(user))
    # if dict is empty
    if({} == users_dict_temp):
        message = 'everyone voted'
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
    await message_to_delete.delete()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('ryuh weekend'):
        members = ''
        msg_sent = await message.channel.send(schedule_weekend_msg)
        msg_id = msg_sent.id
        if(message.channel.id == js_hboss_channel_id):
            f = open("last_scheduled_msg_id.txt", "w")
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
        if(message.channel.id == js_hboss_channel_id):
            f = open("last_scheduled_msg_id.txt", "w")
            f.write(str(msg_id))
            f.close()
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

    if message.content.startswith('ryuh check'):
        f = open("last_scheduled_msg_id.txt", "r")
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