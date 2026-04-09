import requests
import json
import sqlalchemy as db
import os
import pandas as pd
import numpy as np
import time
from requests.exceptions import SSLError, ConnectionError, Timeout
from Alchemy_core import engine, insert, metadata_obj

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

# engine = db.create_engine(DB_URL)
# connection = engine.connect()
metadata_obj.create_all(engine)
metadata_obj.reflect(bind=engine)


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

  response = requests.request(f"POST", url, headers=headers, data=payload, timeout=30, verify=False)

  jresponse = json.loads(response.text)

  if response.status_code == 200:
    print("1. Authorization is complete!")
    return jresponse.get('access_token')
  else:
    print(f"Status code isn't positive: {requests.status_code}")

  
def getLimits(authToken):

  url = "https://be.broker.ru/trade-api-bff-limit/api/v1/limits"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, params=payload, timeout=30, verify=False)

  jresponse = json.loads(response.text)

  for key in jresponse.keys():
    if jresponse.get(f'{key}') != []:
      df_limits = pd.json_normalize(jresponse.get(f'{key}'))
      df_limits.columns = df_limits.columns.str.strip().str.replace(".","")
      with engine.connect() as conn:
        table = metadata_obj.tables[f'{key}']
        result = conn.execute(insert(table), df_limits.to_dict("records"))
        conn.commit()
  

def getPortfolio(authToken):
  url = "https://be.broker.ru/trade-api-bff-portfolio/api/v1/portfolio"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {authToken}'
  }

  response = requests.request("GET", url, headers=headers, data=payload, timeout=30, verify=False)
  # print(response.text)

  if response.status_code == 200:
    jresponse = json.loads(response.text)

    with engine.connect() as conn:
      result = conn.execute(insert(metadata_obj.tables['portfolio']), jresponse)
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

  response = requests.request("GET", url, headers=headers, params=payload, timeout=30, verify=False)

  if response.status_code != 200:
    return f"Error while getDailySchedule! Status code: {response.status_code}"  

  jresponse = json.loads(response.text)
  
  df_daily = pd.DataFrame(jresponse)
  print(df_daily)

def getInstruments(authToken):

  url = "https://be.broker.ru/trade-api-information-service/api/v1/instruments/by-type"

  listTypes = ['CURRENCY', 'STOCK', 'FOREIGN_STOCK', 'BONDS', 'NOTES', 'DEPOSITARY_RECEIPTS', 'EURO_BONDS', 'MUTUAL_FUNDS', 'ETF', 'FUTURES', 'OPTIONS', 'GOODS', 'INDICES']

  for instrument in listTypes:
    pages = 0
    
    while True:
      payload = {
        'type': f'{instrument}',
        'size': '100',
        'page': f'{pages}'
      }
      headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {authToken}'
      }

      try:
        response = requests.request("GET", url, headers=headers, params=payload, timeout=30, verify=False)
      except SSLError:
        print("SSL ошибка, повтор через 5 сек...")
        time.sleep(5)
        response = requests.get(url, headers=headers, params=payload, timeout=30)

      if response.status_code != 200:
        return f"Status code {response.status_code} for getInstruments() is negative!"


      jresponse = json.loads(response.text)

      if len(jresponse) == 0:
        print("Maximum of pages was shown! It is finish!")
        break

      records = []
      records.append(jresponse)
      
      df_instruments = pd.json_normalize(jresponse)
      df_temp_boards = pd.json_normalize(df_instruments["boards"].str[0])
      df_instruments = df_instruments.drop(columns=['excludeTypes','displayNameSecond','excludeTypeFlags','logoLink','promoIdx','boards']).join(df_temp_boards)
      df_instruments.columns = df_instruments.columns.str.strip().str.replace(".","")
      # df_instruments = df_instruments.replace("", None).where(df_instruments.notna(), other=None)
      # print(df_instruments)
      

      with engine.connect() as conn:
        result = conn.execute(insert(metadata_obj.tables['instruments']), df_instruments.where(df_instruments.notna(), other=None).to_dict("records"))
        conn.commit()
        # time.sleep(1)
        
      pages += 1
      
      if len(jresponse) < 100:
        break
  
  
def getAllBids(authToken):

  url = "https://be.broker.ru/trade-api-bff-order-details/api/v1/orders/search"

  page = -1
  while True: 
    print("NEW ITERATION OF WHILE")
    page += 1
    payload = json.dumps({
      "page": f"{page}",
      "size": "100",
      "sort": "orderDateTime,asc",
      "startDateTime": "2026-01-26T00:00:00.000Z",
      "endDateTime": "2026-04-09T20:25:00.000Z",
      # "side": 1,
      # "orderStatus": [
      #   1
      # ],
      # "orderTypes": [
      #   1
      # ],
      # "tickers": [
      #   "string"
      # ],
      # "classCodes": [
      #   "string"
      # ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'Bearer {authToken}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=30, verify=False)
    
    if response.status_code != 200:
      return f"Status code {response.status_code} for getInstruments() is negative!"
    
    jresponse = json.loads(response.text)
    
    for key, item in jresponse.items():
      print(f'{key} -> {item}')
      
    df_allbids = pd.json_normalize(jresponse.get("records"))
    
    # pd.set_option('display.max_columns', None)
    
    print(df_allbids)
    
    with engine.connect() as conn:
      result = conn.execute(insert(metadata_obj.tables['allBids']), df_allbids.where(df_allbids.notna(), other=None).to_dict("records"))
      conn.commit()

    if jresponse.get("totalRecords") < 100:
      break


def searchAllDeals(authToken):

  url = "https://be.broker.ru/trade-api-bff-trade-details/api/v1/trades/search"

  dictSides = {'1': 'Buy', '2': 'Sell'}
  
  for key in dictSides.keys():
    payload = json.dumps({
      "page": "0",
      "size": "100",
      "sort": "tradeDateTime,asc",
      "side": "{key}",
      # "tradeNums": [
      #   0
      # ],
      # "tickers": [
      #   "NMTP"
      # ],
      # "classCodes": [
      #   "TQBR"
      # ],
      "startDateTime": "2026-01-01T00:00:00.000Z",
      "endDateTime": "2026-04-09T20:15:00.000Z"
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': '*/*',
      'Authorization': 'Bearer <token>'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=30, verify=False)

    print(response.text)
    
  



def main():
  bearerToken = doAuthorization()
  getLimits(bearerToken)
  getPortfolio(bearerToken)
  getInstruments(bearerToken)
  getDailySchedule(bearerToken)
  getAllBids(bearerToken)
  # searchAllDeals(bearerToken)

    
if __name__ == '__main__':
  main()