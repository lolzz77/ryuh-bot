import os        
import discord
from module import scheduler
from module import client
from module import version as version_file
from module import testData
from module import error
from module import config
import inspect
import emojis as emoji_v2
import emoji
import re

client = client.client

@client.command()
async def test(ctx):
    """
    test command for testing
    To trigger this command, run `!test`
    in discord chat channel that discord bot has access to
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
async def send(ctx):
    """
    To send message
    Command: !send [channel id] [message]
    Example: !send 839981719754244118 hello world hahaha 
    Observed Result: The bot will send "hello world hahaha" to the channel ID specified.
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))



    message_full_content = ctx.message.content
    message_full_content = message_full_content.split(' ')
    message_full_content.pop(0)
    channel_id_to_send = int(message_full_content[0])
    message_full_content.pop(0)
    message_to_send = ' '.join(message_full_content)

    channel = client.get_channel(channel_id_to_send)

    await channel.send(message_to_send)



@client.command()
async def update(ctx, msg):
    """
    To update the last msg id in the file
    Whenever 'ryuh bot' command is triggered
    It will write the last msg id into the file
    If you call 'ryuh bot' again, the file will be updated again
    If you mistaken it, then you can call this command '!update [msg id]' to update the file
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # get IDs
    channel_id = ctx.channel.id
    last_message_id = msg

    file_path = scheduler.SCHEDULE_PATH + str(channel_id) + '/schedule.txt'
    
    # Check if file exists
    isExist = os.path.exists(file_path)

    # If not, create it
    if(False == isExist):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    f = open(file_path, "w")
    f.write(str(last_message_id))
    f.close()

    await ctx.channel.send('updated')

@client.command()
async def ver(ctx):
    """
    to get current version and send to discord chat
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)

    version = version_file.version
    print(version)

    await channel.send(version)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, msg_id, users_channel_id, schedule_channel_id):
    """
    to check votes
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    message = ''
    bossing_time = ''
    bossing_day = ''
    next_msg = False # to print next msg, intended for emoji use, bigger emoji will appear on new msg that doesn't contain text
    date_pattern = r"\b\d{1,2}/[A-Za-z]{3}/\d{2}\b"

    # Have to do this, else you get error channel has no attribute 'fetch_message'
    # get current channel id
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    try:
        message_to_check = await channel.fetch_message(msg_id)
    except Exception as exception_error:
        error.error_message = 'Fetch last message failed, did you delete my schedule message that I pinged you guys to vote? Run `!update <msg_id> without `<>` to update.'
        await message_to_check.channel.send(error.error_message)
        await message_to_check.channel.send(exception_error)
        return
    
    content = message_to_check.content
    content_split = content.split("\n")

    # Fetch user & schedule data from discord chat
    users_dict = await read_user(users_channel_id)
    if not users_dict:
        await message_to_check.channel.send(error.error_message)
        return
    
    users_dict_temp = users_dict.copy()
    reactions = message_to_check.reactions
    emoji_found = False

    # Show ryuh-bot is typing...
    # 2 approaches:
    # a. ctx.typing()
    # b. message.channel.typing() <- this works both for 'ryuh check' n '!check <msg ID>' cmd
    async with message_to_check.channel.typing(): 
        # Construct result message
        """
        [GuanYinMaday]
        🐱:
        🐹:
        🦁:
        [Friday]
        🐶:
        🐻::ryuh:
        🐯:
        🐰:
        🐼:
        [All Cannot]
        🙃::ryuh:
        everyone voted
        Friday -> 🐻 - 9pm
        All Cannot -> 🙃  - all cannot
        """
        for line in content_split:
            if line.startswith("Emojis detected"):
                continue
            if line == '':
                continue
            if line.startswith("\n"):
                continue
            if re.search(date_pattern, line):
                # Get the first word in the line
                # Eg: Friday - 12/May/25
                # Then, get the "Friday" word
                message += f"[{line.split()[0]}]\n"
                bossing_day = f"{line.split()[0]}"
                continue
            elif line.startswith('All cannot'):
                message += "[All Cannot]\n"
                bossing_day = "All Cannot"
                continue
            
            # Check if the 1st word in the line is emoji or not
            if emoji.is_emoji(line.split()[0]) == False:
                continue
            _emoji = emoji_v2.decode(line.split()[0])
            message += f"{line.split()[0]}:"
            count = 0
            
            # check if this emoji exists in the reaction
            for r in reactions:
                if _emoji == emoji_v2.decode(r.emoji):
                    emoji_found = True
                    break
                else:
                    continue
            if emoji_found == False:
                continue
            if len(reactions) == 0:
                break
            # Get the 1st reaction
            reaction = reactions.pop(0)

            # Check reactions on the message
            async for user in reaction.users():
                # If the user reacted to the message contains in the user dictionary
                if(str(user.id) in users_dict):
                    message += users_dict[str(user.id)]
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
            # this means all users voted
            if count == len(users_dict):
                bossing_time += f"{bossing_day} -> {line}\n"

        # Result: Whether everyone voted or someone didnt vote
        if({} == users_dict_temp):
            message += 'everyone voted'
            message += '\n'

            # check if vote has reached consensus
            if not bossing_time:
                message += "there's no consensus on the bossing date"
                message += '\n'
                # ping everyone
                # if you wan to ping role, '<@&[role_id]>'
                # the differences is '&'
                for user in users_dict:
                    message += '<@' + str(user) + '> '
                message += '\n'
                message += 'how?' 
                next_msg = True
            else:
                message += bossing_time
        else:
            # get discord user ID, append in message, ping them
            for dis_tag in users_dict_temp:
                message += '<@'
                message += str(dis_tag)
                message += '> '
            message += 'oi ' + scheduler.emoji_cat_angery

    msg_sent = await message_to_check.reply(message)
    file_path = scheduler.SCHEDULE_PATH + str(message_to_check.channel.id) + '/schedule_check_result.txt'
    msg_id = write_file(msg_sent, file_path)
    
    if(next_msg):
        message = '' 
        message = scheduler.emoji_monkey_how_1 + scheduler.emoji_monkey_how_2
        await message_to_check.channel.send(message)

@client.command()
async def delete(ctx, arg):
    """
    To delete bot's message
    If the message is not bot's, it wont delete
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    try:
        message_to_delete = await channel.fetch_message(arg)
    except Exception as exception_error:
        error.error_message = 'Fetch last message failed, did you delete it?'
        await ctx.channel.send(error.error_message)
        await ctx.channel.send(exception_error)
        return
    
    if(message_to_delete.author == client.user):
        await message_to_delete.delete()
    else:
        await ctx.channel.send("That message does not belong to me! I won't delete it.")

async def read_user(channel_id):
    """
    given a message: [emoji]/[user ID]
    this func will return [emoji] & [user ID]

    the message format shall be:
    [emoji]/[user ID]
    it will split with '/' symbols
    whitespaces will be removed

    if multiple strings, put new one in newline
    [emoji]/[user ID]
    [emoji]/[user ID]

    function will split each row
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    user_dict = dict()
    user_list = list()

    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    # For this, have to use try, except, it will crash the system
    try:
        message_fetched = await channel.fetch_message(last_message_id)
    except Exception as exception_error:
        error.error_message = 'User list last message fetch failed. Try resend the message again'
        return None
    
    content = message_fetched.content

    # split into individual row
    rows = content.split('\n')

    # split message
    for row in rows:
        """
        User list format:
        <emoji>/<discord ID>/<friendly name>
        The <friendly name> is not used, but is for user to know who is it
        """
        count = row.count('/')
        if count != 2:
            error.error_message = 'Invalid user list. Format: [emoji]/[discord ID]/[friendly name]. For [emoji], either use nitro or type like this \\\<:emoji_name:emoji_id\\\>'
            return None

        row = row.strip() # remove leading & traling whitespaces
        split = row.split('/')
        if not split[0] or not split[1] or not split[2]:
            error.error_message = 'Invalid user list. Format: [emoji]/[discord ID]/[friendly name]. For [emoji], either use nitro or type like this \\\<:emoji_name:emoji_id\\\>'
            return None
        
        # In discord msg, if no nitro, we use <:emoji_name:emoji_id> format
        # When it reads it out, it will become `\\<:emoji_name:emoji_id>`
        # We have to remove the leading `\\`, else it wont print the emoji
        if split[0][:1] == '\\':
            split[0] = split[0][1:]
        user_list.append(split)

    # remove leading n traling whitespaces
    for user in user_list:
        user[0] = user[0].strip()
        user[1] = user[1].strip()
        user_emoji = user[0]
        user_id = user[1]
        """
        dictionary format:
        dict = {'user id' : 'user emoji'}
        """
        user_dict[user_id] = user_emoji

    return user_dict

async def read_schedule(channel_id):
    """
    1. return schedule message with @MONDAY@ replaced with actual date
    2. return list of emoji found in the schedule message
    3. Emoji that use for voting, must be the 1st char of the row
    3. Some emoji cant be detected
    eg: 
    1. :regional_indicator_m:
    2. custom self made added moving emojis
    
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # initialize date, serves as refreshing date as well
    await scheduler.init_date()

    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    try:
        message_fetched = await channel.fetch_message(last_message_id)
    except Exception as exception_error:
        error.error_message = 'Fetch schedule last message failed. Suspect it was deleted, resend it.'
        return None, None

    content = message_fetched.content
    content_split = content.split("\n")
    days_set = {'@MONDAY@','@TUESDAY@','@WEDNESDAY@','@THURSDAY@','@FRIDAY@','@SATURDAY@','@SUNDAY@','all cannot'}
    day = ''
    schedule_template_contain_DAYS_symbol = False

    # check for invalid schedule template
    for symbol in days_set:
        if str(symbol) in content:
            schedule_template_contain_DAYS_symbol = True
            break
    if not schedule_template_contain_DAYS_symbol:
        error.error_message = 'Template does not contain "@DAY@" symbol.'
        return None, None
    emoji_list_decoded = []
    # Get all emojis
    for line in content_split:
        if line == '':
            continue
        if line.startswith("\n"):
            continue
        if emoji.is_emoji(line.split()[0]):
            emoji_list_decoded.append(emoji_v2.decode(line.split()[0]))
    
    if len(emoji_list_decoded) > 20:
        error.error_message = 'Schedule template has more than 20 voting emojis. Discord only allow maximum 20 reactions.'
        return None, None

    # replace '@MONDAY@' symbol to actual date
    # '**' is to bold them in discord
    for day in days_set:
        if day == '@MONDAY@':
            content = content.replace(day, "**" + scheduler.monday + "**")
        elif day == '@TUESDAY@':
            content = content.replace(day, "**" + scheduler.tuesday + "**")
        elif day == '@WEDNESDAY@':
            content = content.replace(day, "**" + scheduler.wednesday + "**")
        elif day == '@THURSDAY@':
            content = content.replace(day, "**" + scheduler.thursday + "**")
        elif day == '@FRIDAY@':
            content = content.replace(day, "**" + scheduler.friday + "**")
        elif day == '@SATURDAY@':
            content = content.replace(day, "**" + scheduler.saturday + "**")
        elif day == '@SUNDAY@':
            content = content.replace(day, "**" + scheduler.sunday + "**")

    schedule_message = f"-# Emojis detected: ({len(emoji_list_decoded)}) {' '.join(emoji_list_decoded)}\n\n"
    schedule_message = schedule_message + content

    return schedule_message, emoji_list_decoded

def write_file(msg_sent, file_path):
    """
    To write data into file
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # Get the schedule msg ID sent by bot, to save in file, for 'ryuh check' command to retrieve
    msg_id = msg_sent.id 

    # Check if file exists
    isExist = os.path.exists(file_path)

    # If not, create it
    if(False == isExist):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    f = open(file_path, "w")
    f.write(str(msg_id))
    f.close()
    return msg_id

def read_file(file_path):
    """
    To read data from a file
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    f = open(file_path, "r")
    msg_id = f.read()
    f.close()
    return msg_id

def tokenizer():
    """
    Return list of emojis from the scheduler.time_list
    Not in used
    """
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
    if config.DEBUG_PRINT_FUNCTION_ENTRY:
        print(str(os.path.abspath(__file__)) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    my_dict = {}
    for item in input_list:
        my_dict[item] = "[Mon]\n" + str(item)
