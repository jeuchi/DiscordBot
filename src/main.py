# main.py
# Author: Jeremy Euchi
# Date: Oct 7, 2021
# Description: Pepega bot used in private server. 
# Commands to print Rainbow Six Siege stats and ask questions.

import random
import discord
from music import Music
from discord.ext.commands.core import after_invoke 
from ubi import R6
from discord.ext import commands
from constants import ASK_RESP, NAME, VERSION, TOKEN

# Build client
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  """
  Initialize when bot is online.
  """
  for guild in client.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send(f'https://cdn.discordapp.com/emojis/792923101179805696.png?size=96')
                await channel.send(f'{NAME} is online! Version: {VERSION}')
  await client.change_presence(activity=discord.Streaming(name="Rainbow Six Siege", url="https://www.twitch.tv/shaiiko"))

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, welcome and type .help for {NAME} commands!'
  )

@client.command()
async def ask(ctx, question=None):
  if question is None:
    await ctx.send(f'https://cdn.discordapp.com/emojis/792923101179805696.png?size=96')
    await ctx.send('Didn\'t type a question!')
    return False

  await ctx.send(f'{random.choice(ASK_RESP)}')

@client.command()
async def git(ctx):
  await ctx.send(f'Version: {VERSION}')
  await ctx.send('https://github.com/jeuchi/DiscordBot')

client.add_cog(Music(client))
client.add_cog(R6(client))
client.run(TOKEN)