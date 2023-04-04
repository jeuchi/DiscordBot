# constants.py
# Author: Jeremy Euchi
# Date: Oct 9, 2021
# Description: Variables to be defined as static across files.

import os
from dotenv import load_dotenv
load_dotenv()

NAME = 'Pepega'
VERSION = '2.00.04'
GITHUB_URL = 'https://github.com/jeuchi/DiscordBot'

TOKEN = os.getenv('DISCORD_TOKEN')
EMAIL = os.getenv('UBIEMAIL')
PASSWORD = os.getenv('UBIPASS')
APP_ID = '3587dcbb-7f81-457c-9781-0e3f29f6f56a'
OPEN_API_KEY = os.getenv('OPEN_API_KEY')
SEASON = 'Commanding Force'

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
        "Gold V",      "Gold IV",     "Gold III",    "Gold II",     "Gold I",
        "Emerald V",   "Emerald IV",  "Emerald III",  "Emerald II", "Emerald I",
        "Platinum V",   "Platinum IV",  "Platinum III",  "Platinum II", "Platinum I",
        "Diamond V",   "Diamond IV",  "Diamond III",  "Diamond II", "Diamond I",
        "Champion"
]

RANK_ICONS = ["https://i.imgur.com/sB11BIz.png",  # unranked

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/copper-5.png",        # copper 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/copper-4.png",        # copper 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/copper-3.png",        # copper 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/copper-2.png",        # copper 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/copper-1.png",        # copper 1

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/bronze-5.png",        # bronze 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/bronze-4.png",        # bronze 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/bronze-3.png",        # bronze 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/bronze-2.png",        # bronze 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/bronze-1.png",        # bronze 1

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/silver-5.png",        # silver 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/silver-4.png",        # silver 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/silver-3.png",        # silver 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/silver-2.png",        # silver 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/silver-1.png",        # silver 1

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/gold-5.png",          # gold 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/gold-4.png",          # gold 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/gold-3.png",          # gold 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/gold-2.png",          # gold 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/gold-1.png",          # gold 1

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/emerald-5.png",       # emerald 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/emerald-4.png",       # emerald 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/emerald-3.png",       # emerald 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/emerald-2.png",       # emerald 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/emerald-1.png",       # emerald 1
              
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/platinum-5.png",      # platinum 5
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/platinum-4.png",      # platinum 4
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/platinum-3.png",      # platinum 3
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/platinum-2.png",      # platinum 2
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/platinum-1.png",      # platinum 1

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/diamond-5.png",       # diamond 5  
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/diamond-4.png",       # diamond 4  
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/diamond-3.png",       # diamond 3  
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/diamond-2.png",       # diamond 2  
              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/diamond-1.png",       # diamond 1 

              "https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/champions.png",        # champion  
]
