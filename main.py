import discord
from discord.ext import commands
import os
import music

cogs = [music]

client = commands.Bot(command_prefix="$", intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)

my_secret = os.environ['BOTTOKEN']
client.run(my_secret)

