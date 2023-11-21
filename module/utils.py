import os        
import discord
from module import scheduler
from module import client
from module import version as version_file
from module import testData
from module import error
import inspect

client = client.client

@client.command()
async def test(ctx):
    """
    test command for testing
    To trigger this command, run `!test`
    in discord chat channel that discord bot has access to
    """
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)

    version = version_file.version
    print(version)

    await channel.send(version)

# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg, users_channel_id, schedule_channel_id):
    """
    to check votes
    """
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    message = ''
    bossing_day = ''
    next_msg = False # to print next msg, intended for emoji use, bigger emoji will appear on new msg that doesn't contain text

    # Have to do this, else you get error channel has no attribute 'fetch_message'
    # get current channel id
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    try:
        message_to_check = await channel.fetch_message(arg)
    except:
        error.error_message = 'Fetch last message failed, did you delete my schedule message that I pinged you guys to vote?'
        await message_to_check.channel.send(error.error_message)
        return
    
    # Fetch user & schedule data from discord chat
    users_dict = await read_user(users_channel_id)
    if not users_dict:
        await message_to_check.channel.send(error.error_message)
        return
    
    users_dict_temp = users_dict.copy()

    # my intention is to fetch the emoji list only
    try:
        schedule_message, emoji_dict = await read_schedule(schedule_channel_id)
    except:
        error.error_message = str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno) + ':Error'
        await message_to_check.channel.send(error.error_message)
        return

    if not schedule_message or not emoji_dict:
        await message_to_check.channel.send(error.error_message)
        return

    # Show ryuh-bot is typing...
    # 2 approaches:
    # a. ctx.typing()
    # b. message.channel.typing() <- this works both for 'ryuh check' n '!check <msg ID>' cmd
    async with message_to_check.channel.typing(): 
        # Check for each reaction
        for reaction in message_to_check.reactions:
            reaction_str = str(reaction)

            # Construct 'day' string
            """
            [MONDAY]         <-------
            [emoji] : [user]
            """
            if reaction_str in emoji_dict:
                day = '[' + emoji_dict[reaction_str] + ']\n'
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
                rows = schedule_message.split('\n')
                for row in rows:
                    # remove leading & trailing whitespaces
                    row = row.strip()
                    if row.startswith(str(reaction_str)):
                        bossing_day += emoji_dict[reaction_str]
                        bossing_day += ' -> '
                        bossing_day += row
                        bossing_day += "!\n"

        # if temp dict is empty
        if({} == users_dict_temp):
            message += 'everyone voted'
            message += '\n'

            # check if vote has reached consensus
            if not bossing_day:
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

@client.command()
async def delete(ctx, arg):
    """
    To delete bot's message
    If the message is not bot's, it wont delete
    """
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    try:
        message_to_delete = await channel.fetch_message(arg)
    except:
        error.error_message = 'Fetch last message failed, did you delete it?'
        await ctx.channel.send(error.error_message)
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
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    user_dict = dict()
    user_list = list()

    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    # For this, have to use try, except, it will crash the system
    try:
        message_fetched = await channel.fetch_message(last_message_id)
    except:
        error.error_message = 'User list last message fetch failed. Try resend the message again'
        return None
    
    content = message_fetched.content

    # split into individual row
    rows = content.split('\n')

    # split message
    for row in rows:
        count = row.count('/')
        if count <= 0:
            error.error_message = 'Invalid user list, does not contain "/"'
            return None
        elif count > 1:
            error.error_message = 'Invalid user list, "/" contains more than 1'
            return None

        row = row.strip() # remove leading & traling whitespaces
        split = row.split('/')
        if not split[0] or not split[1]:
            error.error_message = 'Invalid user list. Please use this format: [emoji]/[discord user ID]'
            return None
            
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

    emoji condition:
    1. emoji has to be the 1st chracter in the row
    2. emoji has to be discord default emoji
    3. emoji cannot be literally num/alphabet like `:one:` emoji
    """
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    try:
        message_fetched = await channel.fetch_message(last_message_id)
    except:
        error.error_message = 'Fetch schedule last message failed. Try resend the schedule again.'
        return None, None
    content = message_fetched.content
    rows = content.split('\n')
    emoji_dict = dict()
    days_set = {'@MONDAY@','@TUESDAY@','@WEDNESDAY@','@THURSDAY@','@FRIDAY@','@SATURDAY@','@SUNDAY@',}
    day = ''
    proceed = False

    # check for invalid emoji (contains '\u')
    # Note: `if '\\u'` will not detect `\u` in the read string
    # `if '\u` will have compile error
    # if you type '\u' in the discord and let it read
    # it will become '\\u' in the read string
    # .encode will not convert '\\u' into '\x'
    # .encode will convert '\u' into '\x'
    # but cant determine which '\x' is exactly the '\u'
    # i guess the best is see if there's 4 '\x' if more than 4, means this emoji contains '\u'

    # check for invalid schedule template
    for symbol in days_set:
        if str(symbol) in content:
            proceed = True
            break
    
    if not proceed:
        error.error_message = 'Template does not contain "@DAY@" symbol'
        return None, None

    # fetch emoji
    for row in rows:
        # for row that contains only new line in it
        if len(row) <= 0:
            continue

        # remove leading & trailing whitespaces
        row = row.strip()

        if any(x in row for x in days_set):
            day = row.split(' ')[0]

        # only can use discord default emoji,
        
        # but cannot use emoji that lietrally is number/alphabet
        # like discord `:one:` emoji will show `1` and this code will treat as number rather than emoji
        
        # Then, if you use custom uploaded emoji, it will be transalted into `<emoji_name:emoji_ID>`
        # then your row[0] will be '<'
        
        # Then, for ':bear:' and ':polar_bear:' emoji
        # they will end up being the same 'bear' emoji
        # cos for :polar_bear:, it will have :bear: + numbers behind
        # this i will impose a minor fix, if key present, put msg "conflict emoji or smthg"
        # nvm, my quick fix is crash the bot
        # so when printing schedule n bot crashed, good, is a sign
        
        # check for emojies
        # only check the 1st char is emoji or not
        
        # for discord, there are 2 types of emojis:
        # 1. default
        # - these emojis if you type `\:smile:` it will output another emoji instead of the emoji ID
        # - these emojis can be detected using 
        # 2. custom emojis
        # - these emojis if you type `\:emoji:` it will output `<emoji_name:emoji_id>`
        # 3. default emoji with skin
        # - :polar_bear: will become `🐻\u200d❄️`
        # - for these type of emoji, u better return fail
        # - note: after encode('utf-8'), \u all these will be converted into '\x' as well

        # when you read text, and the text contains emoji, it will read the `output` version

        # technique to check for emojies
        # - text.encode('utf-8')
        # - only emojies will be converted into '\x' string

        # Condition:
        # Only check the 1st char is emoji or not
        # There might be the msg title contain emojis, those are not counted
        
        # # check whether is custom emoji. Custom emoji = <:emoji_name:emoji_id>
        # if row[0] == '<':
        #     substring = row.split('>')[0]
        #     substring += '>' # split above will not include the '>' itself
        #     emoji_dict[substring] = day
        #     continue

        # for the moment, reject custom emoji first, got problem
        if row[0] == '<':
            error.error_message = 'Schedule tempalte contains custom emoji. Dont use custom emoji, use discord default emoji'
            return None, None

        encoded_first_character = row[0].encode('utf-8') # only check 1st char is emoji or not
        encoded_first_character_string = str(encoded_first_character)
        if '\\x' not in encoded_first_character_string:
            continue
        # if it is emoji, check whether it is valid emoji
        # valid emoji = contain '\x' not more than 4 for row[0] & row[1]
        # because :polar_bear: will be translted into :bear:\u200d:cold:
        # thus, row[0] = :bear:
        # row[1] maybe is '\u' i dk
        # that is, if row[1] is also '\x', then this is invalid emoji
        encoded_second_character = row[1].encode('utf-8') # only check 1st char is emoji or not
        encoded_second_character_string = str(encoded_second_character)
        if '\\x' in encoded_second_character_string:
            error.error_message = 'Template contain invalid emoji.\n'
            error.error_message += 'This row ' + row
            return None, None
        
        # next, before inserting into dictionary, check if got duplicates emoji
        if row[0] in emoji_dict:
            error.error_message = "There's duplicate emojis in the schedule template"
            return None, None

        emoji_dict[row[0]] = day

    if not emoji_dict:
        error.error_message = 'Schedule template has no emoji on the 1st character on any of the rows.'
        return None, None
    
    if len(emoji_dict) > 20:
        error.error_message = 'Schedule template has more than 20 voting emojis. Discord only allow maximum 20 reactions.'
        return None, None

    # replace '@MONDAY@' symbol to actual date
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

    schedule_message = content

    return schedule_message, emoji_dict

def write_file(message, msg_sent):
    """
    To write data into file
    """
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

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
    print(str(os.path.dirname(os.path.abspath(__file__))) + ':' + str(inspect.currentframe().f_code.co_name) + ':' + str(inspect.currentframe().f_lineno))

    my_dict = {}
    for item in input_list:
        my_dict[item] = "[Mon]\n" + str(item)
