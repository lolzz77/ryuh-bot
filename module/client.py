import discord
from discord.ext import commands

# default from discord bot setup tutorial
intents = discord.Intents.default()
intents.message_content = True

# https://stackoverflow.com/questions/73393567/discord-py-client-run-and-bot-run-in-one-code
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)