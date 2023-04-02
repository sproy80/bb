import json
from flask import session
from models import LiveData, Signals, db, app, SwingTrade, WatchList, FutureStockList
import datetime
import pandas as pd

# with app.app_context():
#     db.create_all()


def save_live_data(symbol, open, high, low, close, volume, time_frame):
    with app.app_context():
        data = LiveData.query.filter_by(symbol=symbol).first()

        if data is None:
            data = LiveData()

        data.symbol = symbol
        data.open = open
        data.high = high
        data.low = low
        data.close = close
        data.volume = volume
        data.time_frame = time_frame
        data.timestamp = datetime.datetime.now()
        db.session.add(data)
        db.session.commit()
        return "Success..."


def get_live_data(symbol):
    try:
        with app.app_context():
            sdata = LiveData.query.filter_by(symbol=symbol).all()

            if sdata is None:
                return "No data found"
            else:
                data = {
                    'date': [],
                    'open': [],
                    'high': [],
                    'low': [],
                    'close': [],
                    'volume': []
                }

                data['date'].append(sdata[0].timestamp)
                data['open'].append(sdata[0].open)
                data['high'].append(sdata[0].high)
                data['low'].append(sdata[0].low)
                data['close'].append(sdata[0].close)
                data['volume'].append(sdata[0].volume)

                print(sdata[0].open)

                df = pd.DataFrame(data)

                return df
    except:
        print('Error getting live data')


def add_to_watchlist(symbol, stock_name, stock_id):
    try:
        with app.app_context():
            stock = WatchList(symbol=symbol, stock_name=stock_name,
                              buy_date=datetime.datetime.now(), stock_id=stock_id)
            db.session.add(stock)
            db.session.commit()
            return f"{stock_name} added to WatchList successfully."

    except:
        return f"Error Occured adding {stock_name} . "


def get_watchlist():
    with app.app_context():
        watchlist = WatchList.query.all()
        return watchlist


def get_future_stock_list():
    with app.app_context():
        stocklist = FutureStockList.query.all()
        return stocklist


def add_to_signals(symbol, price, signal_type, time_frame, reason):
    try:
        with app.app_context():
            stock = Signals(signal_time=str(datetime.datetime.now()),
                            symbol=symbol, entry_price=price,
                            signal_type=signal_type, time_frame=time_frame, reason=reason)
            db.session.add(stock)
            db.session.commit()
            return f"{symbol} added to Signals successfully."

    except Exception as err:
        msg = f"Error Occured adding {symbol}. \n Exception : {err} . "
        print(msg)
        return msg


# add_to_signals(symbol='SBIN', price=525.36,
#                signal_type='Sell', time_frame='15', reason='test')


# save_live_data(symbol='TCS', open=10, high=20, low=5,
#                close=40, volume=400, time_frame='15')

# print(get_live_data(symbol='TCS'))
