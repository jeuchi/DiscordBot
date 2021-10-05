import base64
import json
import os
from datetime import datetime, timedelta

import requests

class UbiAuth:
  # Initialize token authentication from email/password and save session.
  #   Email: User's Ubisoft email.
  #   Password: User's Ubisoft password
  def __init__(self, email, password):
    self.token = base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")
    self.appId = '3587dcbb-7f81-457c-9781-0e3f29f6f56a'
    self.getUbiData()

  # Request using authentication and save session token for use in retrieving Ubisoft profiles.
  def getUbiData(self):
    headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic' + self.token,
			'Ubi-AppId': self.appId
		}

    payload = {
      'rememberMe': 'true'
    }

    resp_raw = requests.post('https://public-ubiservices.ubi.com/v3/profiles/sessions', headers=headers, data=payload)

    resp_json = resp_raw.json()
    httpCode = resp_json['httpCode']

    print(resp_json)
    if httpCode != 200:
      print(f'Ubisoft authentication failed with HTTP code: {httpCode}')
      return False
      
    self.ticket = resp_json['ticket']
    self.sessionId = resp_json['sessionId']
    self.sessionKey = resp_json['sessionKey']
    self.spaceId = resp_json['spaceId']
    self.ownUserId = resp_json['userId']
  
  async def getData(self, link):
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Ubi_v1 t=' + self.ticket,
      'Ubi-AppId': self.appId,
      'Ubi-SessionId': self.sessionId,
      'Connection': 'keep-alive',
      'expiration': f'{(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")}.657Z'
    }

    if link:
      async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as r:
          
          if r.status == 200:
            return await r.json()
          else:
            print(f'{Fore.RED}[Error]{Style.RESET_ALL} An error occured: ')
            print(r.reason)
            print(r)
            return False
    else:
      return False