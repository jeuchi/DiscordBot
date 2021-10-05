import base64
import json
import os
from datetime import datetime, timedelta

import requests
from requests.api import head

class UbiAuth:
  # Initialize token authentication from email/password and save session.
  #   Email: User's Ubisoft email.
  #   Password: User's Ubisoft password.
  def __init__(self, email, password):
    self.token = base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")
    self.appId = '3587dcbb-7f81-457c-9781-0e3f29f6f56a'
    self.getUbiData()

  # Request using authentication and save session token for use in retrieving Ubisoft profiles.
  def getUbiData(self):
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
        print("Ubisoft authentification did not return a response")
        return False
    
    resp_json = resp_raw.json()

    if resp_raw.status_code != 200:
        print(resp_json)
        print(f'Ubisoft authentication failed with HTTP code: {resp_raw.status_code}')
        return False
      
    self.ticket = resp_json['ticket']
    self.sessionId = resp_json['sessionId']
    self.sessionKey = resp_json['sessionKey']
    self.spaceId = resp_json['spaceId']
    self.ownUserId = resp_json['userId']
  
  def getData(self, link):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
      'Content-Type': 'application/json',
      'Authorization': 'Ubi_v1 t=' + self.ticket,
      'Ubi-AppId': self.appId,
      'Ubi-SessionId': self.sessionId,
      'Connection': 'keep-alive',
      'expiration': f'{(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")}.657Z'
    }

    if link:
        resp_raw = requests.get(link, headers=headers)
        return resp_raw.json()
    else:
        return False