import asyncio
from asyncio.windows_events import NULL
import json
import os
from socket import MsgFlag
from symtable import Symbol
from urllib import request
from fyers_api import fyersModel
from fyers_api import accessToken
import websockets
import bot_session as fyersSession
from fyers_api.Websocket import ws
import time
import socket
import xlwings as xw
import websocket
import aiofiles
import requests

# from dashboard import consumers
is_maket_live = False

app_id = "B5ZFYFYM0W-100"
secret_key = "MA7YGV5Y67"
is_async = False
log_path = "C:/fyers_log"

access_token = fyersSession.login()

ws_access_token = f"{app_id}:{access_token}"


def get_symbol_data(ws_access_token):

    data_type = "symbolData"
    # # symbol = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX",
    #           "NSE:SBIN-EQ", "NSE:HDFC-EQ", "NSE:IOC-EQ"]

    symbol = ["MCX:CRUDEOIL23APRFUT"]
    print('Program Started....')
    fs = ws.FyersSocket(access_token=ws_access_token,
                        run_background=True, log_path=log_path)
    fs.websocket_data = custom_message

    fs.subscribe(symbol=symbol, data_type=data_type)

    fs.keep_running()


def get_order_update():

    data_type = "orderUpdate"
    fs = ws.FyersSocket(access_token=ws_access_token,
                        run_background=False, log_path=log_path)
    fs.websocket_data = custom_message

    symbol = ["NSE:SBIN-EQ"]
    fs.subscribe(symbol=symbol, data_type=data_type)

    # print('Custom Message ' + custom_message)

    print(fyersSession.positions())

    # trade.fyers.g
    fs.keep_running()

    time.sleep(10)


def custom_message(msg):
    # print(f"Custom:{msg}")
    # data = {
    #     'symbol': msg[0]['symbol']
    # }
    print(msg)
    # show_live_data_in_excel(msg)s
    # time.sleep(60)


get_symbol_data(ws_access_token)
