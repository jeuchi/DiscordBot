# ubi.py
# Author: Jeremy Euchi
# Date: Oct 7, 2021
# Description: API to handle communication to Ubisoft servers
# and retrieve player data and authentication.

import base64
import requests
import random
import os
import time
import discord
from time import strftime, gmtime
from discord.ext import commands
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta
from requests.api import head
from constants import APP_ID, RANK, RANK_ICONS, EMOTES, SEASON

# Ubi authenticate.
email = os.getenv('UBIEMAIL')
password = os.getenv('UBIPASS')

class UbiAuth:
  """
  Ubi authentification using private email/password stored in env variables.
  Methods to initialize and get data by sending GET/POST requests to Ubisoft servers.
  Initialize token authentication from email/password and save session.
  """
  def __init__(self, email='', password=''):
    self.token = base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")
    self.app_id = APP_ID

  def create_ubi_authentication(self):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'Content-Type': 'application/json',
			'Authorization': 'Basic ' + self.token,
			'Ubi-AppId': self.app_id,
      'Connection': 'keep-alive'
		}
    payload = {
      'rememberMe': 'true'
    }
    resp_raw = requests.post('https://public-ubiservices.ubi.com/v3/profiles/sessions', headers=headers, json=payload)

    if (resp_raw is None):
        print("Ubisoft authentification did not return a response.")
        return False
    
    resp_json = resp_raw.json()

    if resp_raw.status_code != 200:
        print(resp_json)
        print(f'Ubisoft authentication failed with HTTP code: {resp_raw.status_code}')
        return False
      
    try:
      self.ticket = resp_json['ticket']
      self.session_id = resp_json['sessionId']
      self.session_key = resp_json['sessionKey']
      self.space_id = resp_json['spaceId']
      self.own_user_id = resp_json['userId']
    except (IndexError, KeyError) as e:
      print('Ubisoft authentication failed decoding session keys.')
      return False
  
  def get_ubi_data(self, link='http://google.com'):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 
      "Upgrade-Insecure-Requests": "1",
      "DNT": "1",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate",
      'Content-Type': 'application/json',
      'Authorization': 'Ubi_v1 t=' + self.ticket,
      'Ubi-AppId': self.app_id,
      'Ubi-SessionId': self.session_id,
      'Connection': 'keep-alive',
      'expiration': f'{(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")}.657Z'
    }
    resp_raw = requests.get(link, headers=headers)

    try:
      resp_json = resp_raw.json()
      return resp_json
    except JSONDecodeError:
      print(f'[get_data] Invalid link: {link}')
      return False
  
  def check_expiration(self, resp_json):
    # Check ticket expiration
    try:
      expired = resp_json['message']
    except:
      expired = False
    
    # If session has expired, reauthenticate
    if expired == 'Ticket is expired':
      print('Ticket expired. Trying again')
      self.authenticated = self.create_ubi_authentication()
      expired = True

    return expired

class Player:
  """
  Store information retrieved from Ubisoft containing 
  fields such as username, wins, losses and K/D.
  """
  def __init__(self):
    self.username = ''
    self.level = 0
    self.play_time = 0
    self.profile_pic = ''
    self.r6_url = ''
    self.mmr = 0
    self.rank = ''
    self.max_rank = ''
    self.kd = 0
    self.wins = 0
    self.losses = 0

  def print_summary(self):
    m, s = divmod(self.play_time, 60)
    h, m = divmod(m, 60)
    embed = discord.Embed(title=SEASON, colour=discord.Color.green())
    embed.set_author(name=self.username, url=self.r6_url, icon_url=self.profile_pic)
    embed.set_thumbnail(url=RANK_ICONS[self.rank])
    embed.add_field(name="Level", value=self.level, inline=True)
    embed.add_field(name="Lifetime", value=f'{h}H', inline=True)
    embed.add_field(name="MMR", value=self.mmr, inline=True)
    embed.add_field(name="K/D", value='{:.2f}'.format(self.kd), inline=True)
    embed.add_field(name="Wins", value=self.wins, inline=True)
    embed.add_field(name="Losses", value=self.losses, inline=True)
    embed.add_field(name=f"Best {SEASON} Rank", value=RANK[self.max_rank], inline=True)
    return embed

class R6(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.ubi = UbiAuth(email=email, password=password)
      self.authenticated = False
      self.cooldown = 0
      
  @commands.command()
  async def r6(self, ctx, username=None, dbg_set=None):
    """
    R6 command. List user stats for current season. Optional dbg for programmers.

    Arguments:
    ctx -- discord context.
    username -- username to search.
    dbg_set -- 'dbg' to display HTTP requests.
    """
    dbg = False

    # Check cooldown. Limit to one request per 5 seconds
    remaining_time = int(time.time() - self.cooldown)
    if remaining_time < 5:
      remaining_time = 5 - remaining_time
      await ctx.send(f'{random.choice(EMOTES)}')
      await ctx.send(f'Wait {remaining_time} second(s)')
      return False
    
    # Check for no username
    if username is None:
      await ctx.send(f'https://cdn.discordapp.com/emojis/792923101179805696.png?size=96')
      await ctx.send('Didn\'t type a username!')
      return False

    if dbg_set == 'dbg':
      dbg = True

    # Reset cooldown
    self.cooldown = time.time()

    # Create session if false
    if self.authenticated is False:
      self.authenticated = self.ubi.create_ubi_authentication()

    if self.authenticated is False:
      await ctx.send('Error authenticating with Ubisoft.')
      return False

    # Request user ID from username given and check for session expiration
    link = f'https://public-ubiservices.ubi.com/v3/profiles?namesOnPlatform={username}&platformType=uplay'
    resp_json = self.ubi.get_ubi_data(link=link)
    expired = self.ubi.check_expiration(resp_json)
    # Try again with new authentication if expired
    if expired:
      resp_json = self.ubi.get_ubi_data(link=link)
    if resp_json is False:
      await ctx.send('Error retrieving player.')
      return False
    if dbg:
      await ctx.send(f'[DEBUG-USER-ID] {resp_json}')

    # Retrieve player's user ID
    player = Player()
    try:
      user_id = resp_json['profiles'][0]['userId']
      player.username = resp_json['profiles'][0]['nameOnPlatform']
    except (IndexError, KeyError) as e:
      await ctx.send('User not found.')
      return False

    # Request player's info
    link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={user_id}'
    resp_json = self.ubi.get_ubi_data(link)
    if resp_json is False:
      await ctx.send('Error retrieving player info.')
      return False
    if dbg:
      await ctx.send(f'[DEBUG-PLAYER] {resp_json}')

    # Create player info from response
    player.profile_pic = f'https://ubisoft-avatars.akamaized.net/{user_id}/default_146_146.png?appId=3587dcbb-7f81-457c-9781-0e3f29f6f56a'
    player.r6_url = f'https://r6.tracker.network/profile/pc/{username}'
    try:
      player.rank = resp_json['players'][user_id]['rank']
      player.max_rank = resp_json['players'][user_id]['max_rank']
      player.mmr = int(resp_json['players'][user_id]['mmr'])
      player.wins = resp_json['players'][user_id]['wins']
      player.losses = int(resp_json['players'][user_id]['losses'])
      kills = resp_json['players'][user_id]['kills']
      deaths = resp_json['players'][user_id]['deaths']
    except (IndexError, KeyError) as e:
      await ctx.send('Error retrieving player info.')
      return False

    # Catch 0 deaths
    try:
      player.kd =  (kills / deaths)
    except ZeroDivisionError:
      player.kd = kills

    # Get player level
    link = f'https://public-ubiservices.ubi.com/v1/profiles/{user_id}/stats/ProgressionClearanceLevel?spaceId=5172a557-50b5-4665-b7db-e3f2e8c5041d'
    resp_json = self.ubi.get_ubi_data(link)
    if resp_json is False:
      await ctx.send('Error retrieving player level.')
      return False
    if dbg:
      await ctx.send(f'[DEBUG-PLAYER-LEVEL] {resp_json}')
    try:
      player.level = resp_json['stats']['ProgressionClearanceLevel']['value']
    except (IndexError, KeyError) as e:
      await ctx.send('Error retrieving player level.')
      return False

     # Get play time in seconds
    link = f'https://public-ubiservices.ubi.com/v1/profiles/stats?profileIds={user_id}&spaceId=5172a557-50b5-4665-b7db-e3f2e8c5041d&statNames=ProgressionPvPTimePlayed'
    resp_json = self.ubi.get_ubi_data(link)
    if resp_json is False:
      await ctx.send('Error retrieving play time.')
      return False
    if dbg:
      await ctx.send(f'[DEBUG-PLAY-TIME] {resp_json}')
    try:
      player.play_time = int(resp_json['profiles'][0]['stats']['ProgressionPvPTimePlayed']['value'])
    except (IndexError, KeyError) as e:
      await ctx.send('Error retrieving play time.')
      return False

    # Create Discord embed summary
    async with ctx.typing():
      summary = player.print_summary()
    await ctx.send(embed=summary)
