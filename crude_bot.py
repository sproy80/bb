from trade import Trade


trade = Trade(symbol='CRUDEOIL23APRFUT',
              exchange='MCX',
              time_frame='15', target=80, stoploss=40, lookback=3)

trade.run_bot()
