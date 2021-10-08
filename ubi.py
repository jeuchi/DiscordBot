# ubi.py
# Author: Jeremy Euchi
# Date: Oct 7, 2021
# Description: API to handle communication to Ubisoft servers
# and retrieve player data and authentication.

import base64
import json
import requests
import discord
import os
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta
from requests.api import head

RANK = ["Unranked",
        "Copper V",   "Copper IV",   "Copper III",   "Copper II",   "Copper I",
        "Bronze V",   "Bronze IV",   "Bronze III",   "Bronze II",   "Bronze I",
        "Silver V",   "Silver IV",   "Silver III",   "Silver II",   "Silver I",
        "Gold III",     "Gold II",     "Gold I",
        "Platinum III", "Platinum II", "Platinum I", 
        "Diamond III", "Diamond II", "Diamond I",
        "Champion"
]

RANK_ICONS = ["https://i.imgur.com/sB11BIz.png",  # unranked

              "https://i.imgur.com/B8NCTyX.png",  # copper 5
              "https://i.imgur.com/ehILQ3i.jpg",  # copper 4
              "https://i.imgur.com/6CxJoMn.jpg",  # copper 3
              "https://i.imgur.com/eI11lah.jpg",  # copper 2
              "https://i.imgur.com/0J0jSWB.jpg",  # copper 1

              "https://i.imgur.com/TIWCRyO.png",   # bronze 5
              "https://i.imgur.com/42AC7RD.jpg",  # bronze 4
              "https://i.imgur.com/QD5LYD7.jpg",  # bronze 3
              "https://i.imgur.com/9AORiNm.jpg",  # bronze 2
              "https://i.imgur.com/hmPhPBj.jpg",  # bronze 1

              "https://i.imgur.com/PY2p17k.png",  # silver 5
              "https://i.imgur.com/D36ZfuR.jpg",  # silver 4
              "https://i.imgur.com/m8GToyF.jpg",  # silver 3
              "https://i.imgur.com/EswGcx1.jpg",  # silver 2
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4guViAQud6vSRPWoWGUNyU/32b279721dcfb09d0668f7b6a15ae3ea/R6S_RANK_500x500_Silver_01.png",    # silver 1

              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/5o6FA0tOweqf2RMm6ly9ET/5cf7d4ce0465315dfa4012a6a84c428a/R6S_RANK_500x500_GOLD_03.png",      # gold 3
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/HQeTsDatqQRo9qW5KKs1x/4ba25d10cfb681d3347985a1125b69cf/R6S_RANK_500x500_GOLD_02.png",       # gold 2
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/8Mpi8OU4AnEh93pVcapyW/2b140e3caae994c8fa2255623cba323e/R6S_RANK_500x500_GOLD_01.png",       # gold 1

              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1NdqJyCZK86i3AnQwEvIlt/68ed7769e4098ec682e8c793f5121722/R6S_RANK_500x500_Platinum_03.png",  # plat 3
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/54T8y7G0Yu6qniIliDAuWz/d7a8d760969db59b1608c255e1674a65/R6S_RANK_500x500_Platinum_02.png",  # plat 2
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/70KhxbY7ZSilFgcMFIFKip/cb5435f1e0e59804f38496868d8e9369/R6S_RANK_500x500_Platinum_01.png",  # plat 1

              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2ynWMUUP5klIyABI8yTxyy/1bcfc19f8142f2c6b4d2e23a1f2387af/RANK_L_Diamond_03.png",             # diamond 3
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1yXN9oMKkeAvgRFR7vZNo8/2efc56be886b09178a7af99ccab8606a/RANK_L_Diamond_02.png",             # diamond 2
              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/3IjRzUddD2cTrx6xdVXFmY/49195f3e71b2d5694b50524bfd8fd30c/R6S_RANK_500x500_Diamond_01.png",   # diamond 1

              "https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/74IhNF2m0VsDiurjYt9Q58/deb07d428a4a25acd70c92f6c7fcfca4/R6S_RANK_500x500_Champions_01.png"  # champion
]

# Ubi authentification using private email/password stored in env variables.
# Methods to initialize and get data by sending GET/POST requests to Ubisoft servers.
class UbiAuth:
  # Initialize token authentication from email/password and save session.
  #   Email: User's Ubisoft email.
  #   Password: User's Ubisoft password.
  def __init__(self, email='', password=''):
    self.token = base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")
    self.appId = '3587dcbb-7f81-457c-9781-0e3f29f6f56a'

  # Request using authentication and save session token for use in retrieving Ubisoft profiles.
  def create_ubi_authentication(self):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'Content-Type': 'application/json',
			'Authorization': 'Basic ' + self.token,
			'Ubi-AppId': self.appId,
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
      self.sessionId = resp_json['sessionId']
      self.sessionKey = resp_json['sessionKey']
      self.spaceId = resp_json['spaceId']
      self.ownUserId = resp_json['userId']
    except (IndexError, KeyError) as e:
      print('Ubisoft authentication failed decoding session keys.')
      return False
  
  # Request data from Ubisoft using link.
  def get_ubi_data(self, link='http://google.com'):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
      'Content-Type': 'application/json',
      'Authorization': 'Ubi_v1 t=' + self.ticket,
      'Ubi-AppId': self.appId,
      'Ubi-SessionId': self.sessionId,
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

# Player object contains all stats retrieved.
class Player:
  def __init__(self):
    self.username = ''
    self.profile_pic = ''
    self.r6_url = ''
    self.mmr = 0
    self.rank = ''
    self.max_rank = ''
    self.kd = 0
    self.wins = 0
    self.losses = 0

  # Print player summary for current season.
  def print_summary(self):
    embed = discord.Embed(title='Crystal Guard', colour=discord.Color.green())
    embed.set_author(name=self.username, url=self.r6_url, icon_url=self.profile_pic)
    embed.set_thumbnail(url=RANK_ICONS[self.rank])
    embed.add_field(name="Rank", value=RANK[self.rank], inline=True)
    embed.add_field(name="MMR", value=self.mmr, inline=True)
    embed.add_field(name="K/D", value='{:.2f}'.format(self.kd), inline=True)
    embed.add_field(name="Wins", value=self.wins, inline=True)
    embed.add_field(name="Losses", value=self.losses, inline=True)
    embed.add_field(name="Max Rank", value=RANK[self.max_rank], inline=True)
  
    return embed