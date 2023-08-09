import os        
import discord
from module import scheduler
from module import client
from module import users
from module import version as version_file

client = client.client

@client.command()
async def test(ctx):
    """
    test command for testing
    """
    # get emoji id by running '\:name:'
    js_bossing_channel = 963160372385296414
    my_discord_general_channel = 803958155935219724
    channel = client.get_channel(my_discord_general_channel)

    # guild = 491039338659053568
    # emoji = discord.utils.get(ctx.guild.emojis, id=811260045307543553)
    # emoji = discord.utils.get(client.emojis, name='Birthday_Cake')
    # await channel.send("<a:Birthday_Cake:811260045307543553>")
    # emoji = client.get_emoji(811260045307543553)
    # await channel.send(emoji)

    # await channel.send("Monday (15 May 23) 10pm! Tele carry y`all!")

    # msg_sent = await message.channel.send("Ryuh! Ryuh! Scammer spotted!")
    # msg_sent = await message.channel.send("Using rate 8/b, 3.33 = ?")
    # msg_sent = await message.channel.send("8 x α = 3.33, α = 3.33/8, α = 0.41625")
    # msg_sent = await message.channel.send("0.41625b x 1000 = 416.25m! Not 415m!!!")

    # msg_id = 1106578766131630140
    # msg_to_react = await channel.fetch_message(msg_id)
    # await msg_to_react.add_reaction("👍")

    # Send image
    # Reply to message method
    # msg_to_reply_id = 1116729780553912392
    # msg_to_reply = await channel.fetch_message(msg_to_reply_id)
    # image = discord.File('./image/peanut.jpg')
    # await msg_to_reply.reply(file = image)

    # No reply method
    # await channel.send(file = image)

@client.command()
async def ver(ctx):
    """
    to get current version and send to discord chat
    """
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)

    version = version_file.version
    print(version)

    await channel.send(version)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg):
    """
    to check votes
    """
    users_dict = users.users_dict
    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    users_dict_temp = users_dict.copy()
    message = ''
    bossing_day = ''
    next_msg = False # to print next msg, intended for emoji use, bigger emoji will appear on new msg that doesn't contain text

    # Have to do this, else you get error channel has no attribute 'fetch_message'
    # get current channel id
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_check = await channel.fetch_message(arg)

    # Show ryuh-bot is typing...
    # 2 approaches:
    # a. ctx.typing()
    # b. message.channel.typing() <- this works both for 'ryuh check' n '!check <msg ID>' cmd
    async with message_to_check.channel.typing(): 
        # Check for each reaction
        for reaction in message_to_check.reactions:
            reaction_str = str(reaction)
            reaction_mapping = scheduler.reaction_mapping

            # Construct string
            if reaction_str in reaction_mapping:
                # I want to print full 'curseday'
                if reaction_mapping[reaction_str][0] == 'Curseday':
                    day = '[' + reaction_mapping[reaction_str][0] + ']\n'
                # For 'All cannot', print full 'Probably OT'
                elif reaction_mapping[reaction_str][0] == 'All cannot':
                    day = '[' + reaction_mapping[reaction_str][1] + ']\n'
                # else, print 1st 3 char only
                else:
                    # From the 'key', get the 1st element from the list, and get 1st 3 character
                    # Essentially, get the 'day' - Mon, Tue, Wed etc
                    day = '[' + reaction_mapping[reaction_str][0][:3] + ']\n'
                # there are multiple emoji on same day, just print the 'day' once
                # e.i: Monday has 2 emojis, this will make sure print 'day' only once
                if day not in message:
                    message += day
                message += reaction_str

            message += " : "
            count = 0

            # Check reactions on the message
            async for user in reaction.users():
                # If the user reacted to the message contains in the user dictionary
                if(str(user.id) in users_dict):
                    message += users_dict[str(user.id)]['emoji']
                    count += 1
                # if is bot itself, dont add the blank emoji
                elif(user == client.user):
                    continue
                # reason to use user_dict_temp, because this will use 'pop' on it
                # then the next loop, it will check the next reaction, then u cannot check on a popped dictionary
                # this popped dictionary is used to keep track who didn't vote
                # you have to put str(), like str(user.id), else python will treat this if as true for all users
                if str(user.id) not in users_dict_temp:
                    continue
                users_dict_temp.pop(str(user.id))

            message += "\n"

            # found a concensus bossing date
            if count == 6:
                bossing_day = " ".join(reaction_mapping[reaction_str])
                bossing_day += "!\n"

        # if temp dict is empty
        if({} == users_dict_temp):
            message += 'everyone voted'
            message += '\n'
            if not bossing_day:
                message += "there's no consensus on the bossing date"
                message += '\n'
                message = '<@&' + str(users.party_role_id) + '>'
                message += '\n'
                message += 'how?' 
                next_msg = True
            else:
                message += bossing_day
        else:
            # get discord user ID, append in message, ping them
            for dis_tag in users_dict_temp:
                message += '<@'
                message += str(dis_tag)
                message += '> '
            message += 'oi ' + scheduler.emoji_cat_angery

    await message_to_check.reply(message)
    
    if(next_msg):
        message = '' 
        message = scheduler.emoji_monkey_how_1 + scheduler.emoji_monkey_how_2
        await message_to_check.channel.send(message)


async def construct_schedule():
    """
    To construct schedule message
    Format:
    Curseday - 13/Jul/23
    🐱 - 8pm
    🐹 - 9pm
    🦁 - 10pm+

    Friday - 14/Jul/23
    ...
    """
    reaction_mapping = scheduler.reaction_mapping
    schedule_message = scheduler.schedule_message
    for reaction in reaction_mapping:
        day = reaction_mapping[reaction][0] # Get day string
        time = reaction_mapping[reaction][1] # Get time

        # Special handling for 'all cannot'
        if day == "All cannot":
            schedule_message += '\n'
            schedule_message += reaction
            schedule_message += ' - '
            schedule_message += day
            continue

        # Print 'Friday - 14/Jul/23'
        if day not in schedule_message:
            schedule_message += '\n'
            schedule_message += day
            schedule_message += ' - '
            schedule_message += '**' # Bold
            
            if(day == 'Thursday' or day == 'Curseday'):
                schedule_message += scheduler.thursday
            if(day == 'Friday'):
                schedule_message += scheduler.friday
            if(day == 'Saturday'):
                schedule_message += scheduler.saturday
            if(day == 'Sunday'):
                schedule_message += scheduler.sunday
            if(day == 'Monday'):
                schedule_message += scheduler.monday
            if(day == 'Tuesday'):
                schedule_message += scheduler.tuesday
            if(day == 'Wednesday'):
                schedule_message += scheduler.wednesday

            schedule_message += '**' # Bold
            schedule_message += '\n'
        
        # Print '🐱 - 8pm'
        schedule_message += reaction
        schedule_message += ' - '
        schedule_message += time
        schedule_message += '\n'

    # Last resort
    schedule_message += '\n'
    schedule_message += 'Wednesday'
    schedule_message += ' - '
    schedule_message += '**' # Bold
    schedule_message += scheduler.wednesday
    schedule_message += '**' # Bold
    schedule_message += '\n'
    schedule_message += 'last resort'

    scheduler.schedule_message = schedule_message

@client.command()
async def delete(ctx, arg):
    """
    To delete bot's message
    If the message is not bot's, it wont delete
    """
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_delete = await channel.fetch_message(arg)
    if(message_to_delete.author == client.user):
        await message_to_delete.delete()
    else:
        await ctx.channel.send("That message does not belong to me! I won't delete it.")

def write_file(message, msg_sent):
    """
    To write data into file
    """
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
    return msg_id

def read_file(message):
    """
    To read data from a file
    """
    file_path = scheduler.SCHEDULE_PATH + str(message.channel.id) + '.txt'
    f = open(file_path, "r")
    msg_id = f.read()
    f.close()
    return msg_id

def tokenizer():
    """
    Return list of emojis from the scheduler.time_list
    Not in used
    """
    token_list = []
    delimiter = "-"
    time_list = scheduler.time_list

    for time in time_list:
        tokens = time.split(delimiter)
        # Append the last character, they are emojis
        # Even if last char is not 'emoji picture', but like '<:pepe_birthday:1087764773615194212>', no problem
        # it will append the whole '<:pepe_birthday:1087764773615194212>' and in discord will be converted into emoji
        token_list.append(tokens[-1])

    return token_list

def make_dict(input_list):
    """
    make dictionary
    Not fisnihed, discontinued
    """
    my_dict = {}
    for item in input_list:
        my_dict[item] = "[Mon]\n" + str(item)