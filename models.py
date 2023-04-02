import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from fyers_bot import history as fyersHistory
# from yahoo_fin import history as yahooHistory
# from fyers_bot import bot_session
from flask_cors import CORS, cross_origin
# from fyers_bot import fyers_trade
##########################################################

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/trade_analysis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

#########################################################


class LiveData(db.Model):
    __tablename__ = 'live_data'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Text, nullable=False, )
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.datetime.utcnow)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    time_frame = db.Column(db.Text)


def __init__(self, symbol, open, high, low, close, volume, time_frame):
    self.symbol = symbol
    self.open = open
    self.high = high
    self.low = low
    self.close = close
    self.volume = volume
    self.time_frame = time_frame


def __repr__(self):
    return f"symbol: {self.symbol}, date:{self.timespan}, open:{self.open} ,high:{self.high}, low:{self.low}, close:{self.close}, volume:{self.volume}, time_frame:{self.time_frame}"


###########################################################


class SwingTrade(db.Model):
    __tablename__ = 'swing_trade'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Text, nullable=False)
    stocks_name = db.Column(db.Text, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float)
    pnl = db.Column(db.Float)
    buy_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    quantity = db.Column(db.Integer, nullable=True, default=0)


def __init__(self, symbol, stock_name, buy_price, buy_date, quantity):
    self.symbol = symbol
    self.stock_name = stock_name
    self.buy_price = buy_price
    self.buy_date = buy_date
    self.qunatity = quantity


def __repr__(self):
    return f"Data : {self.symbol}"


##################################################

class WatchList(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Text, nullable=False)
    stock_name = db.Column(db.Text, nullable=False)
    buy_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    stock_id = db.Column(db.Text, nullable=False)

    def __init__(self, symbol, stock_name, buy_date, stock_id):
        self.symbol = symbol
        self.stock_name = stock_name
        self.buy_date = buy_date
        self.stock_id = stock_id

    def __repr__(self):
        return f"Data : {self.symbol}"

#################################################################################################


class FutureStockList(db.Model):
    __tablename__ = 'future_stock_list'

    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.Text, nullable=False)
    symbol = db.Column(db.Text, nullable=False)
    tv_symbol = db.Column(db.Text, nullable=False)

    def __init__(self, symbol, stock_name, tv_symbol):
        self.stock_name = stock_name
        self.symbol = symbol
        self.symbol = tv_symbol

    def __repr__(self):
        return f"symbol : {self.symbol}, tv_symbol : {self.tv_symbol}"


#################################################################################################

class Signals(db.Model):
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    signal_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.datetime.utcnow)
    symbol = db.Column(db.Text, nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    signal_type = db.Column(db.Text, nullable=False)
    time_frame = db.Column(db.Text)
    reason = db.Column(db.Text)

    def __init__(self, signal_time, symbol, entry_price, signal_type, time_frame, reason=""):
        self.signal_time = signal_time
        self.symbol = symbol
        self.entry_price = entry_price
        self.signal_type = signal_type
        self.time_frame = time_frame
        self.reason = reason

    def __repr__(self):
        return f"symbol : {self.symbol}"

################################################################################################


@ app.route('/')
def index():
    return ("Hello Botbuddy!!!")


# @ app.route('/api/login')
# def login():
#     return bot_session.login()


# @ app.route('/api/getfunds')
# def get_fund_details():
#     return fyers_trade.get_fund_details()


# @ app.route('/api/getpositions')
# def get_all_positions():
#     return fyers_trade.get_positions()


# @ app.route('/api/getuser')
# def get_user_profile():
#     return fyers_trade.get_user_profile()


# @ app.route('/api/getholdings')
# def get_holdings():
#     return fyers_trade.get_holdings()


# @ app.route('/api/placeorder', methods=['POST'])
# def place_order():
#     stock = request.values.get("stock")
#     limitprice = request.values.get("limitprice")
#     # print(stock)
#     return fyers_trade.place_order(stock=stock, limitprice=limitprice)


# @ app.route('/api/save_live_data', methods=['POST'])
# def save_live_data():
#     live_feed = request.values.get("live_feed")
#     print(live_feed)
#     # return live_feed
#     return manager_db.save_live_data(live_feed)


# @ app.route('/api/tv/historicaldata', methods=['POST'])
# def get_historical_data_from_tv():
#     symbol = request.values.get("symbol")
#     exchange = request.values.get("exchange")
#     return tvHistory.get_data(symbol=symbol, exchange=exchange)


# @ app.route('/api/fyers/historicaldata', methods=['POST'])
# def get_historical_data_from_fyers():
#     symbol = request.values.get("symbol")
#     exchange = request.values.get("exchange")

#     # print("symbol :" + symbol + " exchange : " + exchange)
#     return fyersHistory.get_historical_data(symbol=symbol, exchange=exchange)


# @ app.route('/api/yahoo/historicaldata', methods=['POST'])
# def get_historical_data_from_yahoo():
#     symbol = request.values.get("symbol")
#     # exchange = request.values.get("exchange")
#     return yahooHistory.get_history(symbol=symbol)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(threaded=True)
