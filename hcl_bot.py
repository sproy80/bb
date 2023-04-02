from datetime import date, timedelta, time, datetime
import time
from fyers_bot import history as fyersHistory
from strategies import superEma
import pandas as pd
from bb_logging import write_log, write_error_log
from manager_db import add_to_signals
from fyers_bot import indicators

isActiveBuyTrade = False
isActiveSellTrade = False

symbol = 'HCLTECH'
exchange = 'NSE'
resolution = '3'
# DATE FORMAT : 2023-03-22 - YYYY-MM-DD
range_form = str(date.today() - timedelta(days=1))
range_to = str(date.today())


def run_bot():
    signal = 'No Signal'
    print(f"\n Bot Started at {datetime.now()} \n")
    df = fyersHistory.get_historical_data(
        symbol=symbol, exchange=exchange, resolution=resolution, range_form=range_form, range_to=range_to)

    # indicators.supertrend(df)
    # df['datetime'] = pd.to_datetime(df['date'], unit='s')
    # df.to_csv('dt.csv')
    print(df.tail(5))
    if (isActiveBuyTrade or isActiveSellTrade):

        signal = chk_for_exit(df)
    else:

        signal = chk_for_entry(df)


def chk_for_exit(df):
    global isActiveBuyTrade
    global isActiveSellTrade
    result = 'No Signal'
    decision = superEma.trade_decision(df)
    print(str(decision))
    price = decision['close'].values[0]

    if (decision['EMA_Signal'].values == 'Green' and isActiveSellTrade == True):
        msg = str(datetime.now(
        )) + '====================Exit Sell Trade=================================' + '\n'
        msg += str(decision)
        write_log(f"{symbol}_log.txt", msg)
        result = 'exit sell'
        isActiveSellTrade == False
        add_to_signals(symbol=symbol,
                       price=price, signal_type=result)

    if (decision['EMA_Signal'].values == 'Red' and isActiveBuyTrade == True):
        msg = str(datetime.now(
        )) + '====================Exit Buy Trade=================================' + '\n'
        msg += str(decision)
        write_log(f"{symbol}_log.txt", msg)
        result = 'exit buy'
        isActiveBuyTrade = False
        add_to_signals(symbol=symbol,
                       price=price, signal_type=result)

    return result


def chk_for_entry(df):
    global isActiveBuyTrade
    global isActiveSellTrade
    result = 'No Signal'
    decision = superEma.trade_decision(df)
    print(str(decision))
    price = decision['close'].values[0]

    if (decision['Final_Signal'].values == 'Sure Buy' and isActiveBuyTrade == False and isActiveSellTrade == False):
        msg = str(datetime.now(
        )) + '====================Buy Order=================================' + '\n'
        msg += str(decision)
        write_log(f"{symbol}_log.txt", msg)
        result = 'buy'
        isActiveBuyTrade = True
        add_to_signals(symbol=symbol,
                       price=price, signal_type=result)

    if (decision['Final_Signal'].values == 'Sure Sell' and isActiveBuyTrade == False and isActiveSellTrade == False):
        msg = str(datetime.now(
        )) + '====================Sell Order=================================' + '\n'
        msg += str(decision)
        write_log(f"{symbol}_log.txt", msg)
        result = 'sell'
        isActiveSellTrade = True
        add_to_signals(symbol=symbol,
                       price=price, signal_type=result)

    return result


while True:
    try:
        run_bot()
    except Exception as ex:
        print('Error Occured...')
        write_error_log(f"{symbol}_error.txt",
                        f"Error Time : {datetime.now()} \n Error Details : {ex} \n")

    print("\n")
    print(f"Active Buy Trade :- {isActiveBuyTrade}")
    print(f"Active Sell Trade :- {isActiveSellTrade}")
    print(f'\n\n{symbol} Bot is running ...')
    print("=" * 80)
    time.sleep(5)
