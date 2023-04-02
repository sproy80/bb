from trade import Trade
from provider import data_provider

trade = Trade(provider=data_provider.YFIN,
              symbol='CONCOR',
              exchange='NSE',
              time_frame='5m',
              target=5,
              stoploss=5,
              lookback=3, sleep=10)

trade.run_bot()
