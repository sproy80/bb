from flask import Flask, request
import requests
from fyers_bot import bot_session
from fyers_bot import fyers_trade
import os
# from tradingview import history as tvHistory
from fyers_bot import history as fyersHistory
from yahoo_fin import history as yahooHistory
import manager_db
from flask_cors import CORS, cross_origin

pwd = "sanjay@786"
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/trade_analysis"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# app.run(threaded=True)


@ app.route('/')
def index():
    return ("Hello Botbuddy!!!")


@ app.route('/api/login')
def login():
    return bot_session.login()


@ app.route('/api/getfunds')
def get_fund_details():
    return fyers_trade.get_fund_details()


@ app.route('/api/getpositions')
def get_all_positions():
    return fyers_trade.get_positions()


@ app.route('/api/getuser')
def get_user_profile():
    return fyers_trade.get_user_profile()


@ app.route('/api/getholdings')
def get_holdings():
    return fyers_trade.get_holdings()


@ app.route('/api/placeorder', methods=['POST'])
def place_order():
    stock = request.values.get("stock")
    limitprice = request.values.get("limitprice")
    # print(stock)
    return fyers_trade.place_order(stock=stock, limitprice=limitprice)


@ app.route('/api/save_live_data', methods=['POST'])
def save_live_data():
    live_feed = request.values.get("live_feed")
    print(live_feed)
    # return live_feed
    return manager_db.save_live_data(live_feed)


# @ app.route('/api/tv/historicaldata', methods=['POST'])
# def get_historical_data_from_tv():
#     symbol = request.values.get("symbol")
#     exchange = request.values.get("exchange")
#     return tvHistory.get_data(symbol=symbol, exchange=exchange)


@ app.route('/api/fyers/historicaldata', methods=['POST'])
def get_historical_data_from_fyers():
    symbol = request.values.get("symbol")
    exchange = request.values.get("exchange")

    # print("symbol :" + symbol + " exchange : " + exchange)
    return fyersHistory.get_historical_data(symbol=symbol, exchange=exchange)


@ app.route('/api/yahoo/historicaldata', methods=['POST'])
def get_historical_data_from_yahoo():
    symbol = request.values.get("symbol")
    # exchange = request.values.get("exchange")
    return yahooHistory.get_history(symbol=symbol)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(threaded=True)
