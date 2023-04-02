from time import sleep
from os import system, name
import os
import time
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

print(tradingview_ta.__version__)


def get_data(symbol, exchange, screener):
    handler = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener=screener,
        interval=Interval.INTERVAL_1_MINUTE,
        timeout=None
    )

    analysis = handler.get_analysis()
    return analysis
    # open = analysis.indicators['open']
    # high = analysis.indicators['high']
    # low = analysis.indicators['low']
    # close = analysis.indicators['close']
    # EMA5 = analysis.indicators['EMA5']
    # EMA10 = analysis.indicators['EMA10']
    # EMA20 = analysis.indicators['EMA20']
    # EMA50 = analysis.indicators['EMA50']
    # EMA200 = analysis.indicators['EMA200']

    # print(f"Open : {open} High : {high} Low : {low} Close : {close}")

    # print(
    #     f"EMA5 : {EMA5} EMA10 : {EMA10} EMA20 : {EMA20} EMA50 : {EMA50} EMA200 : {EMA200}")
    # print("----------------------------------------------------------------------------")


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# while True:
#     get_data()
#    # time.sleep()
