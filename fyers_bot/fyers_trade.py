import time
from fyers_api import fyersModel
from fyers_api import accessToken
from . import bot_session as fyersSession

app_id = "B5ZFYFYM0W-100"
secret_key = "MA7YGV5Y67"
is_async = False
log_path = "C:/fyers_log"

access_token = fyersSession.login()

# # Creating an instance of fyers model in order to call the apis
fyers = fyersModel.FyersModel(
    token=access_token, is_async=is_async, log_path=log_path, client_id=app_id)

# Setting the AccessToken
fyers.token = access_token


def place_order(exchange, stock, limitprice=0, type=2, side=1):

    symbol = ""
    if (exchange == 'NSE'):
        symbol = exchange + ":" + stock + "-EQ"

    if (exchange == 'MCX'):
        symbol = exchange + ":" + stock

    # stock = 'concor'
    data = {
        "symbol": symbol,
        "qty": 1,
        "type": type,  # Market Order
        "side": side,  # 1 - Buy  2 - Sell
        "productType": "INTRADAY",
        "limitPrice": limitprice,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }

    # data = {"symbol": "MCX:SILVER22SEPFUT",
    #         "qty": 1,
    #         "type": 1,
    #         "side": 1,
    #         "productType": "INTRADAY",
    #         "limitPrice": 61050,
    #         "stopPrice": 0,
    #         "disclosedQty": 0,
    #         "validity": "DAY",
    #         "offlineOrder": "False",
    #         "stopLoss": 0,
    #         "takeProfit": 0
    #         }

    # print(data)
    # // Placing order
    resp = fyers.place_order(data)
    print(resp)
    return resp


def get_user_profile():
    res = fyers.get_profile()
    print(res)
    return res


def get_order_book_with_id(id):
    data = {"id": "NSE:CONCOR-EQ-INTRADAY"}
    return fyers.orderbook(data=data)


# Get Fund Details
def get_fund_details():
    return fyers.funds()


# print(get_fund_details())

# Get Holdings
def get_holdings():
    return fyers.holdings()


# Get intraday positions only
def get_positions():
    res = fyers.positions()
    # print(res)
    return res


def exit_by_id(id):
    data = {
        "id": id
    }
    return fyers.exit_positions(data)


def exit_all():
    exitData = {}
    return fyers.exit_positions(exitData)

# print(fyers.tradebook())

# Check Position
# while True:
#     print(fyers.positions())
#     time.sleep(5)
# Place order
# -------------------------------------------


# // Exit Order
# exitData = {}
# fyers.exit_positions(exitData)

# print(place_order('concor', 709))

# print(get_holdings())

# print(place_order(exchange='NSE', stock='IGL', type=2))

# positions = fyers.positions()['netPositions']


# for pos in positions:
#     print(pos['id'])
#     exit_by_id(pos['id'])
#     time.sleep(10)
