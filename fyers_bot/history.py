from . import bot_session as fyersSession
from . import credentials
from strategies import superEma
from fyers_api import fyersModel
from fyers_api import accessToken
import pandas as pd
import talib
import pandas_ta as ta
import os
import sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

is_async = False
log_path = "C:/fyers_log"

# Get Access Toke
access_token = fyersSession.login()

# # Creating an instance of fyers model in order to call the apis
fyers = fyersModel.FyersModel(
    token=access_token, is_async=is_async, log_path=log_path, client_id=credentials.app_id)

# Setting the AccessToken
fyers.token = access_token

#######################################################


def get_historical_data(symbol, exchange, resolution='15', date_format='1', range_form='2023-03-10', range_to='2023-03-10', cont_flag='1'):

    if exchange == 'NSE':
        symbol = symbol + '-EQ'

    # "range_from": "2022-04-02" - For daywise testing
    data = {"symbol": exchange + ":" + symbol,
            "resolution": resolution,
            "date_format": date_format,
            "range_from": range_form,
            "range_to": range_to,
            "cont_flag": cont_flag}

    # print(data)

    stock_data = fyers.history(data)

    print(stock_data)

    df = pd.DataFrame(stock_data['candles'])
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    df['date'] = pd.to_datetime(df['date'], unit='s', utc=True).map(
        lambda x: x.tz_convert('Asia/Kolkata'))

    return df


# get_historical_data(symbol='SBIN')
