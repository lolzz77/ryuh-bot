import os        
import discord
from module import scheduler
from module import client
from module import users
from module import version as version_file
from module import testData

client = client.client

@client.command()
async def test(ctx):
    """
    test command for testing
    To trigger this command, run `!test`
    in discord chat channel that discord bot has access to
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

    # Fetch user & schedule data from discord chat
    users_dict = await read_user(testData.my_discord_ryuh_bot_channel_user)
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

    # my intention is to fetch the emoji list only
    schedule_message, emoji_list = await read_schedule(testData.my_discord_ryuh_bot_channel_schedule)

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
            if reaction_str in emoji_list:
                day = '[' + emoji_list[reaction_str] + ']\n'
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
            if count == 6:
                bossing_day = " ".join(emoji_list[reaction_str])
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
            
            if(day == 'Thursday' or day == 'Curseday' or day == 'GuanYinMaday'):
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
    user_dict = dict()
    user_list = list()

    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    message_fetched = await channel.fetch_message(last_message_id)
    content = message_fetched.content

    # split into individual row
    rows = content.split('\n')

    # split message
    for row in rows:
        user_list.append(row.split('/'))

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
    # fetch channel & message
    channel = client.get_channel(channel_id)
    last_message_id = channel.last_message_id
    message_fetched = await channel.fetch_message(last_message_id)
    content = message_fetched.content
    rows = content.split('\n')
    emoji_list = dict()
    days_set = {'@MONDAY@','@TUESDAY@','@WEDNESDAY@','@THURSDAY@','@FRIDAY@','@SATURDAY@','@SUNDAY@',}
    day = ''

    # fetch emoji
    for row in rows:
        # for row that contains only new line in it
        if len(row) <= 0:
            continue

        if any(x in row for x in days_set):
            day = row.split(' ')[0]

        # only can use discord default emoji,
        # but cannot use emoji that lietrally is number/alphabet
        # like discord `:one:` emoji will show `1` and this code will treat as number rather than emoji
        # Then, if you use custom uploaded emoji, it will be transalted into `<emoji_name:emoji_ID>`
        # then your row[0] will be '<'
        if not row[0].isalnum():
            emoji_list[row[0]] = day

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

    return schedule_message, emoji_list

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