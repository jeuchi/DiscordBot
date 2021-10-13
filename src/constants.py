# constants.py
# Author: Jeremy Euchi
# Date: Oct 9, 2021
# Description: Variables to be defined as static across files.

import os
from dotenv import load_dotenv
load_dotenv()

NAME = 'Pepega'
VERSION = '2.00.02'
TOKEN = os.getenv('DISCORD_TOKEN')
EMAIL = os.getenv('UBIEMAIL')
PASSWORD = os.getenv('UBIPASS')
APP_ID = '3587dcbb-7f81-457c-9781-0e3f29f6f56a'
SEASON = 'Crystal Guard'

ASK_RESP = ['Outlook is trash bruh',
            'Yeah...idk cuh',
            'LOOKING POGGERS DUD',
            'N <:OMEGALUL:792923100931948585>',
            'Maybe? Leave me alone',
            'YEP',
            'No and ur bad + ratio + L',
            'Maybe in a different universe',
            'Honestly, yeah',
            'YESSSSS',
            'Probably not',
            'Probably tbh'
]

EMOTES = ['https://cdn.discordapp.com/emojis/894659685049856100.png?size=96', # WeirdChamp
          'https://cdn.discordapp.com/emojis/893378054695559188.png?size=96', # Shaiiko
          'https://cdn.discordapp.com/emojis/893376956400304128.png?size=96', # cmonBruh
          'https://cdn.discordapp.com/emojis/894659579990921226.png?size=96', # pepeAgony
          'https://cdn.discordapp.com/emojis/792923101179805696.png?size=96', # Pepega
          'https://cdn.discordapp.com/emojis/792923101129474079.png?size=96', # FeelsGoodMan
]

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