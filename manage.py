import strategies.superEma as sta
import fyers_bot.history as fyersHistory
import pandas as pd
import manager_db

pd.options.mode.chained_assignment = None  # default='warn'

# stock_data = fyersHistory.get_historical_data(symbol='VERTOZ')

# df = pd.DataFrame(stock_data['candles'])

# print(sta.trade_decision(df=df))

sdata = manager_db.get_live_data(symbol='TCS')

print(sdata)
