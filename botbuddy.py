

from trade import Trade
from provider import data_provider

trade = Trade(provider=data_provider.TRADINGVIEW,
              symbol='CRUDEOIL23APRFUT',
              exchange='MCX',
              time_frame='1',
              sleep=0, target=20, stoploss=10, lookback=1, price_tolerance=10)

trade.run_bot()
