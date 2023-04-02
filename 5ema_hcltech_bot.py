import datetime
import json
import os
from fyers_api import fyersModel
from fyers_api import accessToken
from fyers_bot import bot_session as fyersSession
from fyers_bot import credentials
from fyers_api.Websocket import ws
import time
import pandas as pd
import manager_db

is_async = False
log_path = "C:/fyers_log"
app_id = credentials.app_id
secret_key = credentials.secret_key

# ---------------Login--------------------------------------------
access_token = fyersSession.login()
ws_access_token = f"{app_id}:{access_token}"

# ---------------------------------------------------------------

opens = []
highs = []
lows = []
closes = []
volumes = []


def run_bot():

    print(f"Bot Started at {datetime.datetime.now()}")
# -------------------------------Get Symbol Data ----------------------------
    data_type = "symbolData"
   # symbol = ["NSE:TCS-EQ"]
    symbol = ["MCX:CRUDEOIL23APRFUT"]

    # symbol = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX",
    #           "NSE:HCLTECH-EQ", "NSE:HDFCBANK-EQ", "NSE:CONCOR-EQ", "MCX:CRUDEOIL23APRFUT"]

    fs = ws.FyersSocket(access_token=ws_access_token,
                        run_background=False, log_path=log_path)

    fs.websocket_data = custom_message

    fs.subscribe(symbol=symbol, data_type=data_type)

    fs.keep_running()


def run_order_update():

    data_type = "symbolData"
    fs = ws.FyersSocket(access_token=ws_access_token,
                        run_background=False, log_path=log_path)
    fs.websocket_data = custom_message

    fs.subscribe(data_type=data_type)

    print('Custom Message ' + custom_message)

    # trade.fyers.g
    fs.keep_running()


def save_to_db(data):
    open = data['min_open_price']
    high = data['min_high_price']
    low = data['min_low_price']
    close = data['ltp']
    volume = data['min_volume']
    symbol = data['symbol']

    symbol = symbol.replace('NSE:', '')
    symbol = symbol.replace('MCX:', '')
    symbol = symbol.replace('-EQ', '')
    symbol = symbol.replace('-INDEX', '')

    print(close)
    manager_db.save_live_data(symbol=symbol, open=open, high=high,
                              low=low, close=close, volume=volume, time_frame='1')
    return ('Success...')


def custom_message(msg):
    data = msg[0]
    save_to_db(data=data)
    # print(data)
   # time.sleep(10)


run_bot()
