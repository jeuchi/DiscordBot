# bot.py
import os
import random
import time

import discord
from ubi import UbiAuth
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

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

# Ubi authenticate
email = os.getenv('UBIEMAIL')
password = os.getenv('UBIPASS')
ubi = UbiAuth(email=email, password=password)

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  global cooldown
  cooldown = time.time()

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, you can go pog yourself!'
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
async def r6(ctx, username):
  global cooldown
  remaining_time = int(time.time() - cooldown)
  if remaining_time < 10:
    remaining_time = 10 - remaining_time
    await ctx.send(f'Cooldown, wait {remaining_time} second(s)')
    return False

  cooldown = time.time()

  link = f'https://public-ubiservices.ubi.com/v3/profiles?namesOnPlatform={username}&platformType=uplay'
  resp_json = ubi.getData(link)

  userId = resp_json['profiles'][0]['userId']
  link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={userId}'

  resp_json = ubi.getData(link)

  mmr = resp_json['players'][userId]['mmr']
  kills = resp_json['players'][userId]['kills']
  deaths = resp_json['players'][userId]['deaths']

  kd_ratio_seasonal =  (kills / deaths)
  kd_ratio_seasonal_str = '{:.2f}'.format(kd_ratio_seasonal)

  if (mmr < 3200):
    await ctx.send(f'[MMR - {mmr}] LOL NOT EVEN PLAT 3')
  elif (mmr < 2500):
    await ctx.send(f'[MMR - {mmr}] Down bad yikes...')
  else:
    await ctx.send(f'[MMR - {mmr}] Not bad!')

  if (kd_ratio_seasonal >= 1):
    await ctx.send(f'[KD Seasonal - {kd_ratio_seasonal_str}] EZ Clap')
  elif (kd_ratio_seasonal > 0.5):
    await ctx.send(f'[KD Seasonal - {kd_ratio_seasonal_str}] Always dead I guess...')
  else:
    await ctx.send(f'[KD Seasonal - {kd_ratio_seasonal_str}] OMG QUIT THE GAME YIIIIIKES')
   
client.run(TOKEN)