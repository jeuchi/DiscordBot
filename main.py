# bot.py
import os
import random
import time

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

cooldown = 0

# Ubi authenticate.
email = os.getenv('UBIEMAIL')
password = os.getenv('UBIPASS')

# Build client.
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  global cooldown
  cooldown = time.time()

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, welcome and type .help for Pepega commands!'
  )

@client.command()
async def ask(ctx, *, question):
  await ctx.send(f'{random.choice(ASK_RESP)}')

@client.command()
async def clear(ctx, amount=10):
  await ctx.channel.purge(limit=amount)

# R6 command
#   MMR    
#   KD ratio seasonal
@client.command()
async def r6(ctx, username=None, dbg_set=None):
  global cooldown
  dbg = False

  # Check cooldown.
  remaining_time = int(time.time() - cooldown)
  if remaining_time < 10:
    remaining_time = 10 - remaining_time
    await ctx.send('https://cdn.discordapp.com/emojis/894659685049856100.png?size=96')
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

  # Create Ubi authentication to avoid expiration.
  ubi = UbiAuth(email=email, password=password)

  # Request user ID from username given.
  link = f'https://public-ubiservices.ubi.com/v3/profiles?namesOnPlatform={username}&platformType=uplay'
  resp_json = ubi.get_data(link)

  if resp_json is False:
    await ctx.send('Invalid link.')
    return False
  
  if dbg:
    await ctx.send(f'[DEBUG-USER-ID] {resp_json}')

  # Retrieve player's user ID.
  player = Player()
  try:
    userId = resp_json['profiles'][0]['userId']
    player.username = resp_json['profiles'][0]['nameOnPlatform']
  except IndexError:
    await ctx.send('User not found.')
    return False

  link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={userId}'

  resp_json = ubi.get_data(link)

  if resp_json is False:
    await ctx.send('Invalid link.')
    return False

  if dbg:
    await ctx.send(f'[DEBUG-PLAYER] {resp_json}')

  # Create player info.
  try:
    player.rank = resp_json['players'][userId]['rank']
    player.mmr = int(resp_json['players'][userId]['mmr'])
    player.wins = resp_json['players'][userId]['wins']
    player.losses = int(resp_json['players'][userId]['losses'])
    kills = resp_json['players'][userId]['kills']
    deaths = resp_json['players'][userId]['deaths']
  except (IndexError, KeyError) as e:
    await ctx.send('Unable to find player info.')
    return False
  
  # Catch 0 deaths.
  try:
    player.kd_ratio_seasonal =  (kills / deaths)
  except ZeroDivisionError:
    player.kd_ratio_seasonal = kills
    return False

  summary = player.print_summary()
  await ctx.send(embed=summary)

client.run(TOKEN)