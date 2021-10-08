# main.py
# Author: Jeremy Euchi
# Date: Oct 7, 2021
# Description: Pepega bot used in private server. 
# Commands to print Rainbow Six Siege stats and ask questions.

import os
import random
import time
import discord 
from ubi import UbiAuth, Player
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Globals.
TOKEN = os.getenv('DISCORD_TOKEN')

ASK_RESP = ['Outlook is trash bruh',
            'Yeah...idk cuh',
            'LOOKING POGGERS DUD',
            'N <:OMEGALUL:792923100931948585>',
            'Maybe? stfu leave me alone',
            'YEP',
            'No and ur ugly + ratio + L',
            'Maybe in a different universe'
]

EMOTES = ['https://cdn.discordapp.com/emojis/894659685049856100.png?size=96', # WeirdChamp
          'https://cdn.discordapp.com/emojis/893378054695559188.png?size=96', # Shaiiko
          'https://cdn.discordapp.com/emojis/893376956400304128.png?size=96', # cmonBruh
          'https://cdn.discordapp.com/emojis/894659579990921226.png?size=96', # pepeAgony
          'https://cdn.discordapp.com/emojis/792923101179805696.png?size=96', # Pepega
          'https://cdn.discordapp.com/emojis/792923101129474079.png?size=96', # FeelsGoodMan
]

cooldown = 0

# Ubi authenticate.
email = os.getenv('UBIEMAIL')
password = os.getenv('UBIPASS')

# Build client.
client = commands.Bot(command_prefix='.')

# Initialize when bot is online.
@client.event
async def on_ready():
  global cooldown
  cooldown = time.time()
  await client.change_presence(activity=discord.Streaming(name="Rainbow Six Siege", url="https://www.twitch.tv/shaiiko"))

# Introduce new member.
@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, welcome and type .help for Pepega commands!'
  )

# Ask command. Responds with random answer to question.
@client.command()
async def ask(ctx, *, question):
  await ctx.send(f'{random.choice(ASK_RESP)}')

# R6 command. List user stats for current season. Optional dbg for programmers
@client.command()
async def r6(ctx, username=None, dbg_set=None):
  global cooldown
  dbg = False

  # Check cooldown. Limit to one request per 5 seconds.
  remaining_time = int(time.time() - cooldown)
  if remaining_time < 5:
    remaining_time = 5 - remaining_time
    await ctx.send(f'{random.choice(EMOTES)}')
    await ctx.send(f'Wait {remaining_time} second(s)')
    return False
  
  # Check for no username.
  if username is None:
    await ctx.send('Didn\'t type a username Pepega!')
    return False

  if dbg_set == 'dbg':
    dbg = True

  # Reset cooldown.
  cooldown = time.time()

  # Create Ubi authentication to avoid ticket expiration.
  ubi = UbiAuth(email=email, password=password)
  authenticated = ubi.create_ubi_authentication()

  if authenticated is False:
    await ctx.send('Error authenticating with Ubisoft.')
    return False

  # Request user ID from username given.
  link = f'https://public-ubiservices.ubi.com/v3/profiles?namesOnPlatform={username}&platformType=uplay'
  resp_json = ubi.get_ubi_data(link=link)
  if resp_json is False:
    await ctx.send('Error retrieving player.')
    return False
  if dbg:
    await ctx.send(f'[DEBUG-USER-ID] {resp_json}')

  # Retrieve player's user ID.
  player = Player()
  try:
    userId = resp_json['profiles'][0]['userId']
    player.username = resp_json['profiles'][0]['nameOnPlatform']
  except (IndexError, KeyError) as e:
    await ctx.send('User not found.')
    return False

  # Request player's info.
  link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={userId}'
  resp_json = ubi.get_ubi_data(link)
  if resp_json is False:
    await ctx.send('Error retrieving player.')
    return False
  if dbg:
    await ctx.send(f'[DEBUG-PLAYER] {resp_json}')

  # Create player info from response.
  player.profile_pic = f'https://ubisoft-avatars.akamaized.net/{userId}/default_146_146.png?appId=3587dcbb-7f81-457c-9781-0e3f29f6f56a'
  player.r6_url = f'https://r6.tracker.network/profile/pc/{username}'
  try:
    player.rank = resp_json['players'][userId]['rank']
    player.max_rank = resp_json['players'][userId]['max_rank']
    player.mmr = int(resp_json['players'][userId]['mmr'])
    player.wins = resp_json['players'][userId]['wins']
    player.losses = int(resp_json['players'][userId]['losses'])
    kills = resp_json['players'][userId]['kills']
    deaths = resp_json['players'][userId]['deaths']
  except (IndexError, KeyError) as e:
    await ctx.send('Error retrieving player.')
    return False

  # Catch 0 deaths.
  try:
    player.kd =  (kills / deaths)
  except ZeroDivisionError:
    player.kd = kills

  # Create Discord embed summary.
  summary = player.print_summary()
  await ctx.send(embed=summary)

client.run(TOKEN)