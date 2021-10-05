# bot.py
import os
import random

import discord
from ubi import UbiAuth
from discord.ext import commands

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

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  print(f'{client.user.name} has connected to Discord!')

  # Ubi authenticate
  email = os.getenv('UBIEMAIL')
  password = os.getenv('UBIPASS')
  ubi = UbiAuth(email=email, password=password)
  user = "SecretingJuicer"
  link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={user}'

  #ubi.ticket = "t=ewogICJ2ZXIiOiAiMSIsCiAgImFpZCI6ICIzNTg3ZGNiYi03ZjgxLTQ1N2MtOTc4MS0wZTNmMjlmNmY1NmEiLAogICJlbnYiOiAiUHJvZCIsCiAgInNpZCI6ICJhZDkwYTI0YS02MjU4LTQzNjMtYjdlMi0yYjM5YzQyYWZmMWYiLAogICJ0eXAiOiAiSldFIiwKICAiZW5jIjogIkExMjhDQkMiLAogICJpdiI6ICItLWdTeFBTdFZqTjktYS00d3gyMVRRIiwKICAiaW50IjogIkhTMjU2IiwKICAia2lkIjogIjRjYmVhMzE1LWNlMmMtNGVmOS04MjM3LTc5ZjgyN2U5ZjRmOCIKfQ.brortHyBDIKc8p0m9JdrQyYsFDIBJTA9sHYLeYNxX_5IbbN9rY_w218nGhT8AjTiifeSr7Pjyye6dsZzOQ86GpC8vKLtVI2JAHwSn9Ys702P2uBRrJO652-LIGyvrrs8_HFHeE8jhUNSS4Q0_yRce1g_e9AuL9YOwi1qdrwXMLCdbmtqKRQIkY4d4UbqKT3ClhDyvmDJ8qzcO6fcL0aP5DavTIKakuv24IelALQ9mHtLjQUERB3e9cpv67Z4x4CzE8aYPPqNs2O_BUYNKWXnwe9zwwh_d7-Cp0M2U8iZm20YyXyTx_HHZcRBMMcqedUlVQCL9am_4I97xV0lXzUngqNDKeAOJsUaxvZVjeczkYygMRvASZjLq7x7Ky5gZHknNPKT_bZQHgJ2TyyD_usFEYfzKz8SoiP0pfYPA7HGhuNJgc_VDEuh2jZtDWsAewW8AL12ZKgJDtS2sbPp2svn0U-IoNJxD1nbAwqc4LnNCuRpM4yFm65JIRV5hdvGKFqC2aaUQDdvaqi7hRRF-pxRuAMcO0y17i02ePlQdn79kzdm8dKhP5rmwIBu5vfEqDNeOqJ_IEE_NOjhw3ShtekBe9pQN1hnM1gYdrqWowABubNaAzZNeaU_Dk22LPXhWQMiHfUpXPC67leA2IHrEoGcoD1vDaJndDDVsTPNYimPDeyyGMEZ5AFdQlNnAeVjBwZGfi0XgBHGAYIbS_EApacSvxkC9PiKslrNrTmN09ff9NJLafSKengH2SowRgejiNAQiOfi0EpnCptJ9ZGEWu28zO-mpUELPdtxI5sfQRQN9Ldzv4KPLanjxer96jd9gSIiXLkocyGiaUdbFAxo7DztmZ5Vx4EjLL0_NySXEcvOBsI9ruxGCIbl0RU0PgD9QKLgTAuQhh0KOUidhslCPwx-qDnj7_2IzHCpBj5BET6xHD4Rd3UyrBedETKJyDtnqmXXrRzhAQcfz0hjfwHs_TaTdhQ4vsKzrpeDiNWykoMoxwIkTcZV9Kv-qndNEysC_kcJ4K6yzktIMTD9ipmj2o9b4VQWfFg-5pjzEpXutlq43136aCd7ABUqNJySHkiMNLUbSxcsj0SIHWCvPMZsLuZnxlA4P2vYeyuXS6XuqGAZh_I.yVThZidT73On2I8rsMH7k_4vOXuTH20DP7cwyRCTxsU"
  #ubi.sessionId="ad90a24a-6258-4363-b7e2-2b39c42aff1f"
  #await ubi.getData(string)

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

@client.command()
async def r6(ctx, user):
  return 

client.run(TOKEN)