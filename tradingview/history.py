import csv
import itertools
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import pandas_ta as ta
import time


username = 'roysanjay3'
password = 'Tradingview@786'

tv = TvDatafeed(username, password)

# crudeoil_data = None


def get_historicadata(symbol, exchange, time_frame):

    if time_frame == '1':
        interval = Interval.in_1_minute

    if time_frame == '5':
        interval = Interval.in_5_minute

    if time_frame == '15':
        interval = Interval.in_15_minute

    sdata = tv.get_hist(symbol=symbol, exchange=exchange,
                        interval=interval, n_bars=1000, fut_contract=1)
    df = pd.DataFrame(sdata)

   # print(df)

    df.to_csv('stock.csv')

    fdf = pd.read_csv('stock.csv', usecols=[
                      'datetime', 'open', 'high', 'low', 'close', 'volume'])

    fdf.rename(columns={'datetime': 'date'}, inplace=True)

    # print(fdf)

    return fdf


# get_data('CRUDEOIL', 'MCX')
