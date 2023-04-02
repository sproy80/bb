from trade import Trade


trade = Trade(symbol='HDFCBANK',
              exchange='NSE',
              time_frame='5',
              interval=10,
              target=5,
              stoploss=5, lookback=3)

trade.run_bot()
