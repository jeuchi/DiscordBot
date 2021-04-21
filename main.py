# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, you can go fuck yourself!'
  )

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  pepega_quotes = [
    '😂 HE SAID JOY LOOOL',
    'WDYM JANOAH',
    'psdkfpsdfkpsdkfpsdkfpsdkf',
    'any milkers?',
    'WHAT JUICER',
  ]

  sadge_quotes = [
    'i guess...',
    'he\'s never on...',
    'FUCK',
    'on my blicky?',
  ]

  # @Pepega
  if message.content == '<@!834247179870666777>':
    response = random.choice(pepega_quotes)
    await message.channel.send(response)

  # Detecting messages
  elif '😂' in message.content.lower():
    response = '😂 im 12'
    await message.channel.send(response)
  elif 'sadge' in message.content.lower():
    response = random.choice(sadge_quotes)
    await message.channel.send(response)
  elif 'pepega' in message.content.lower():
    response = 'RING RING? SUSHI SUSHI ALLIGATOR.'
    await message.channel.send(response)
  elif 'ready' in message.content.lower():
    response = 'stfu janoah hes busy'
    await message.channel.send(response)
  elif 'omegalul' in message.content.lower():
    response = '<:OMEGALUL:792923100931948585> ❓'
    await message.channel.send(response)
  elif '4heed' in message.content.lower():
    response = 'SO FUNNY DUD'
    await message.channel.send(response)        
  elif message.content == 'raise-exception':
      raise discord.DiscordException

client.run(TOKEN)