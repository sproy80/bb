from fyers_bot import history as fyersHistory

from yahoo_fin import history as yfHistory

from tradingview import history as tvHistory
import pandas as pd

import manager_db

# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo] yf interval


class data_provider():
    def __init__(self) -> None:
        pass

    FYERS = 'fyers'
    YFIN = 'yf'
    TRADINGVIEW = 'tv'


def get_data(provider: data_provider, symbol, exchange, period, time_frame, range_from, range_to):

    data = "No Data"
    if provider == 'fyers':
        hdata = fyersHistory.get_historical_data(
            symbol=symbol, exchange=exchange, resolution=time_frame, range_form=range_from, range_to=range_to)

    if provider == 'yf':
        hdata = yfHistory.get_history(
            symbol=symbol, period=period, interval=time_frame)

    if provider == 'tv':
        if symbol.find('CRUDEOIL') > -1:
            tvsymbol = 'CRUDEOIL'
        else:
            tvsymbol = symbol

        hdata = tvHistory.get_historicadata(
            symbol=tvsymbol, exchange=exchange, time_frame=time_frame)

    # print(data)

    ldata = manager_db.get_live_data(symbol=symbol)

    df = pd.concat([hdata, ldata], ignore_index=True)

    # print(df)

    return df


# data = yfHistory.get_history(symbol='TCS')

# print(data)
