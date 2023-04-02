import csv
import datetime
import itertools
import threading
import time
# from tradingview import history as tvHistory
from strategies import superEma
import pandas as pd
from logging import write_log, write_error_log
from manager_db import *
import yfinance as yf
import numpy as np

# stock_list = ['SBIN', 'HDFCBANK', 'TCS', 'INFY']

# stock_list = get_future_stock_list()
tickers = get_future_stock_list()

# for stock in tickers:
#     print(stock.tv_symbol)


def main():
    # for stock in stock_list:
    #     run_bot(symbol=stock.tv_symbol, exchange='NSE')
    for ticker in tickers:
        tickr = ticker.symbol + '.NS'
        print(f"Pulling data for {tickr}")
        df = yf.download(tickr, group_by="Ticker",
                         period='2d', interval='15m')
        df['symbol'] = ticker.symbol

        df.to_csv('stock.csv')

        dff = pd.read_csv('stock.csv', usecols=[
                          'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'symbol'])
        # x = threading.Thread(target=run_bot(df), args=(1,))
        # x.start()
        # x.join()
        run_bot(dff)


def run_bot(df):
    # df = tvHistory.get_data(symbol=symbol, exchange=exchange)
    print(f"\n Bot Started at {datetime.datetime.now()}")
    # write_log(f"\n Bot Started at {datetime.datetime.now()}")
    try:
        # Converting all the header name into lower case
        df.columns = [x.lower() for x in df.columns]
       # print(df)
        df = superEma.trade_decision_yf(df)
    except Exception as err:
        print(f"EMA ERROR : {err}")

    decision = df
    final_signal = decision['Final_Signal'].values
    symbol = decision['symbol'].values[0]
    close = df['close'].apply(np.ceil).values[0]

    print(str(decision))
    # exit
    # print(f"Close : {df['close']}")
    #    await asyncio.Message.send_message('Bot sending message')
    if (final_signal == 'Sure Buy'):
        msg = str(datetime.datetime.now(
        )) + '====================Buy Order=================================' + '\n'
        msg += str(decision)
        # write_log(msg)
        print(msg)

        add_to_signals(symbol=symbol,
                       price=close, signal_type='Buy')

    if (final_signal == 'Sure Sell'):
        msg = str(datetime.datetime.now(
        )) + '====================Sell Order=================================' + '\n'
        msg += str(decision)
        # write_log(msg)
        print(msg)
        add_to_signals(symbol=symbol,
                       price=close, signal_type='Sell')


try:
    main()
except Exception as ex:
    print(ex)
