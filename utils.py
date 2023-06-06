import os        
import scheduler
import client
import users

client = client.client

@client.command()
async def test(ctx):
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
    send = utils.tokenizer()
    await channel.send(send)

    # js_bossing_channel = 963160372385296414
    # channel = client.get_channel(js_bossing_channel)
    # await channel.send("Monday (15 May 23) 10pm! Tele carry y`all!")

    # msg_sent = await message.channel.send("Ryuh! Ryuh! Scammer spotted!")
    # msg_sent = await message.channel.send("Using rate 8/b, 3.33 = ?")
    # msg_sent = await message.channel.send("8 x α = 3.33, α = 3.33/8, α = 0.41625")
    # msg_sent = await message.channel.send("0.41625b x 1000 = 416.25m! Not 415m!!!")

    # js_bossing_channel = 963160372385296414
    # channel = client.get_channel(js_bossing_channel)
    # msg_id = 1106578766131630140
    # msg_to_react = await channel.fetch_message(msg_id)
    # await msg_to_react.add_reaction("👍")


# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
@client.command()
async def check(ctx, arg):
    users_dict = users.users_dict
    # you have to use .copy()
    # else anything u chg on _temp will affect on the ori dict also
    users_dict_temp = users_dict.copy()
    message = ''
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
        # Check for each reaction
        for reaction in message_to_check.reactions:
            reaction_str = str(reaction)
            reaction_mapping = scheduler.reaction_mapping

            # Construct string
            if reaction_str in reaction_mapping:
                # I want to print full 'curseday' and 'probably OT'
                if reaction_mapping[reaction_str][0] == 'Curseday' or reaction_mapping[reaction_str][0] == 'Probably OT':
                    day = '[' + reaction_mapping[reaction_str][0] + ']\n'
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

@client.command()
async def delete(ctx, arg):
    cur_ch_id = ctx.channel.id
    channel = client.get_channel(cur_ch_id)
    message_to_delete = await channel.fetch_message(arg)
    if(message_to_delete.author == client.user):
        await message_to_delete.delete()
    else:
        await ctx.channel.send("That message does not belong to me! I won't delete it.")

def write_file(message, msg_sent):
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
    file_path = scheduler.SCHEDULE_PATH + str(message.channel.id) + '.txt'
    f = open(file_path, "r")
    msg_id = f.read()
    f.close()
    return msg_id

# Return list of emojis from the scheduler.time_list
# Not in used
def tokenizer():
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

# make dictionary
# Not fisnihed, discontinued
def make_dict(input_list):
    my_dict = {}
    for item in input_list:
        my_dict[item] = "[Mon]\n" + str(item)