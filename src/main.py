# main.py
# Author: Jeremy Euchi
# Date: Oct 7, 2021
# Description: Pepega bot used in private server. 
# Commands to print Rainbow Six Siege stats and ask questions.

import asyncio
import random
import discord
from music import Music
from discord.ext.commands.core import after_invoke 
from ubi import R6
from chatgpt import *
from discord.ext import commands
from constants import ASK_RESP, NAME, VERSION, TOKEN, GITHUB_URL

# Build client
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.',intents=intents)

async def main():
  await client.add_cog(Music(client))
  await client.add_cog(R6(client))
  await client.start(TOKEN)

@client.command()
async def git(ctx):
  embed = discord.Embed(title=f'Patch {VERSION} notes', colour=discord.Color.green())
  async with ctx.typing():
    embed.set_author(name='GitHub link', url=GITHUB_URL)
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/792923101179805696.png?size=96')
    embed.description = '- Added AI\n- Ubisoft is still updating API so latest season is incorrect.'
  await ctx.send(embed=embed)

@client.event
async def on_ready():
  """
  Initialize when bot is online.
  """
  #for guild in client.guilds:
        #for channel in guild.text_channels :
            #if str(channel) == "general" :
                #await git(channel)
  await client.change_presence(activity=discord.Streaming(name="Rainbow Six Siege", url="https://www.twitch.tv/shaiiko"))

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, welcome and type .help for {NAME} commands!'
  )
        
@client.event
async def on_message(message):
  if not client.user.mentioned_in(message):
    await client.process_commands(message)
    return
  
  response = generate_response(message.id, message.content)
  
  # Send the response back to the user
  await message.channel.send(response)

asyncio.run(main())

