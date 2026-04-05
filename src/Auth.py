import requests
import json
import sqlalchemy as db
import os
import pandas as pd
import numpy as np
from Alchemy_core import engine, insert,portfolio
from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

# engine = db.create_engine(DB_URL)
# connection = engine.connect()

def doAuthorization():
  url = "https://be.broker.ru/trade-api-keycloak/realms/tradeapi/protocol/openid-connect/token"
  payload = {
      'client_id': 'trade-api-read',
      'refresh_token': f'{API_KEY}',
      'grant_type': 'refresh_token'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  jresponse = json.loads(response.text)

  if response.status_code == 200:
    print("1. Authorization is complete!")
    return jresponse.get('access_token')
  else:
    print(f"Status code isn't positive: {requests.status_code}. Finished!")
    return 0
  

def getLimits(authToken):

  url = "https://be.broker.ru/trade-api-bff-limit/api/v1/limits"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, params=payload)

  jresponse = json.loads(response.text)

  # print(jresponse)

  # for key in jresponse:
  #   print(f'{key}: {jresponse[key]}')

  # for key, items in jresponse.items():
  #   print(f'=====> {key}')
  #   for item in items:
  #     print(f'{key} -> {item}')
      # for field in item.items():
        

  # print(response.text)


def getPortfolio(authToken):
  url = "https://be.broker.ru/trade-api-bff-portfolio/api/v1/portfolio"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  # print(response.text)

  if response.status_code == 200:
    jresponse = json.loads(response.text)
    with engine.connect() as conn:
      result = conn.execute(insert(portfolio), jresponse)
      conn.commit()
  else:
    print(f"Status code {response.status_code} for getPortfolio() is negative! ")
    return 0


def getDailySchedule(authToken):

  url = "https://be.broker.ru/trade-api-information-service/api/v1/trading-schedule/daily-schedule"

  payload = {
    'classCode': 'TQBR',
    'ticker': 'X5'
  }
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, params=payload)

  print("4. Daily info")
  print(response.text)


def getInstruments(authToken):

  url = "https://be.broker.ru/trade-api-information-service/api/v1/instruments/by-type"

  payload = {
    'type': 'STOCK',
    'size': '1000'
  }
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, params=payload)
  jresponse = json.loads(response.text)

  for item in jresponse:
    for key, value in item.items():
      print(f'{key}: {value}')


def getDeals(authToken, sideDeal):

  url = "https://be.broker.ru/trade-api-bff-trade-details/api/v1/trades/search"

  payload = json.dumps({
    "side": f"{sideDeal}",
    "tradeNums": [
      0
    ],
    "tickers": [
      "SBER"
    ],
    "classCodes": [
      "string"
    ],
    "startDateTime": "2024-07-29T15:51:28.071Z",
    "endDateTime": "2024-07-29T15:51:28.071Z"
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)



def main():
  bearerToken = doAuthorization()
  # getLimits(bearerToken)
  getPortfolio(bearerToken)
  # print('====================================================')
  # getInstruments(bearerToken)


  # typeDeal =   input("Введите тип сделки: 1 - покупка; 2 - продажа -> ")
  # match typeDeal:
  #   case "1":
  #     getDailySchedule(bearerToken, typeDeal)
  #   case "2":
  #     getDailySchedule(bearerToken, typeDeal)
  #   case _:
  #     print(f"Something was wrong: {typeDeal}")
  


    
if __name__ == '__main__':
  main()