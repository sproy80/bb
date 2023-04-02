
import pandas as pd
import pandas_ta as ta
import numpy as np
import talib
pd.options.mode.chained_assignment = None  # default='warn'


def trade_decision(df: pd.DataFrame):

    # df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']
    ############################################ EMA#######################################
    df['EMA_9'] = ta.ema(df['close'], length=9)
    df['EMA_21'] = ta.ema(df['close'], length=21)
    df['EMA_55'] = ta.ema(df['close'], length=55)
    df['EMA_200'] = ta.ema(df['close'], length=200)

########################################## Super Trend#############################
    df['Supertrend'] = ta.supertrend(
        df['high'], df['low'], df['close'], length=10, multiplier=3)['SUPERT_10_3.0']

    # -------------------------------------------

    df['EMA_Signal'] = ''
    df['Sup_Signal'] = ''
    df['Final_Signal'] = ''

    # -----------------------------------------------------
    n = 10
    for i in range(n, len(df)):
        # and df['EMA_21'][i] > df['EMA_55'][i]:
        if df['EMA_9'][i] > df['EMA_21'][i]:
            df['EMA_Signal'][i] = 'Green'
        if df['EMA_9'][i] < df['EMA_21'][i]:
            df['EMA_Signal'][i] = 'Red'

    # -------------------------------------------------

    n = 10
    for i in range(n, len(df)):
        if df['close'][i] > df['Supertrend'][i]:
            df['Sup_Signal'][i] = 'Green'

        if df['close'][i] <= df['Supertrend'][i]:
            df['Sup_Signal'][i] = 'Red'

        # if df['close'][i] > df['Supertrend'][i-1] and df['close'][i-1] <= df['Supertrend'][i-1]:
        #     df['Sup_Signal'][i] = 'Buy'

        # if df['close'][i] < df['Supertrend'][i-1] and df['close'][i-1] >= df['Supertrend'][i-1]:
        #     df['Sup_Signal'][i] = 'Sell'

################################## Final Decision##########################################
    # df['Final_Signal'] = 'No Signal'
    n = 10
    for i in range(n, len(df)):
        if (df['EMA_Signal'][i] == 'Green' and (df['Sup_Signal'][i] == 'Green' or df['Sup_Signal'][i] == 'Green')) and (df['EMA_Signal'][i-1] == 'Red' or df['Sup_Signal'][i-1] == 'Red'):
            df['Final_Signal'][i] = 'Sure Buy'
        else:
            df['Final_Signal'][i] = 'NA'

        if (df['EMA_Signal'][i] == 'Red' and (df['Sup_Signal'][i] == 'Red' or df['Sup_Signal'][i] == 'Red')) and (df['EMA_Signal'][i-1] == 'Green' or df['Sup_Signal'][i-1] == 'Green'):
            df['Final_Signal'][i] = 'Sure Sell'

    curr_bar = df.iloc[len(df) - 1]
    prev_bar = df.iloc[len(df) - 2]

    curr_bar_index = len(df) - 1

    prev_bar_index = curr_bar_index - 1

    # df['Final_Signal'][curr_bar_index] = str(
    #     df["Final_Signal"][prev_bar_index])

    if (prev_bar.Final_Signal == 'Sure Buy' or prev_bar.Final_Signal == 'Sure Sell'):

        if (curr_bar.EMA_Signal == prev_bar.EMA_Signal and curr_bar.Sup_Signal == prev_bar.Sup_Signal):

            print("\n Continuing with previous signals.....")
            df['Final_Signal'][curr_bar_index] = str(
                df["Final_Signal"][prev_bar_index])
        else:
            print('Changed EMA or Sup Signal')
    else:
        print('Changed Final Signal')
    # last_row = df.tail(1)

    # print("Last Row {0}", last_row['Final_Signal'].values)

    return df
    # return df


# -----------------------------------------------------------------------------------------------------------------


def new_trade_decision(df: pd.DataFrame):

    # df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']
    ############################################ EMA#######################################
    df['ema_9'] = ta.ema(df['close'], length=9)
    df['ema_21'] = ta.ema(df['close'], length=21)
    df['ema_55'] = ta.ema(df['close'], length=55)
    df['ema_200'] = ta.ema(df['close'], length=200)

########################################## Super Trend#############################
    df['supertrend'] = ta.supertrend(
        df['high'], df['low'], df['close'], length=10, multiplier=3)['SUPERT_10_3.0']

    # -------------------------------------------

    df['cross_9_21'] = 'no'
    df['cross_9_55'] = 'no'
    df['cross_21_55'] = 'no'
    df['cross_21_200'] = 'no'
    df['cross_55_200'] = 'no'
    df['cross_price_9'] = 'no'
    df['cross_price_21'] = 'no'
    df['cross_price_55'] = 'no'
    df['cross_price_200'] = 'no'

    df['sup_signal'] = 'NA'
    df['event'] = 'NA'
    df['final_signal'] = 'NA'

    # -----------------------------------------------------
    n = 10
    for curr in range(n, len(df)):
        prev = curr - 1

        # ---------------------------EMA 9 CROSS EMA 21 LINE------------------------
        if df['ema_9'][curr] > df['ema_21'][curr]:
            df['cross_9_21'][curr] = 'green'

        if df['ema_9'][curr] < df['ema_21'][curr]:
            df['cross_9_21'][curr] = 'red'

        # ---------------------------EMA 21 CROSS EMA 55------------------------
        if df['ema_21'][curr] > df['ema_55'][curr]:
            df['cross_21_55'][curr] = 'green'

        if df['ema_21'][curr] < df['ema_55'][curr]:
            df['cross_21_55'][curr] = 'red'

        # ---------------------------EMA 21 CROSS EMA 200------------------------
        if df['ema_21'][curr] > df['ema_200'][curr]:
            df['cross_21_200'][curr] = 'green'

        if df['ema_21'][curr] < df['ema_200'][curr]:
            df['cross_21_200'][curr] = 'red'

        # ---------------------------EMA 55 CROSS EMA 200------------------------
        if df['ema_55'][curr] > df['ema_200'][curr]:
            df['cross_21_200'][curr] = 'green'

        if df['ema_55'][curr] < df['ema_200'][curr]:
            df['cross_55_200'][curr] = 'red'

        # ---------------------------PRICE CROSS EMA 9------------------------
        if df['close'][curr] > df['ema_9'][curr]:
            df['cross_price_9'][curr] = 'green'

        if df['close'][curr] <= df['ema_9'][curr]:
            df['cross_price_9'][curr] = 'red'

        # ---------------------------PRICE CROSS EMA 21------------------------
        if df['close'][curr] > df['ema_21'][curr] and (df['cross_price_21'][prev] == 'red'):
            df['cross_price_21'][curr] = 'green'

        if (df['close'][curr] <= df['ema_21'][curr]) and (df['cross_price_21'][prev] == 'green'):
            df['cross_price_21'][curr] = 'red'

        # ---------------------------PRICE CROSS EMA 55------------------------
        if (df['close'][curr] > df['ema_55'][curr]) and df['cross_price_55'][prev] == 'red':
            df['cross_price_55'][curr] = 'green'

        if (df['close'][curr] <= df['ema_55'][curr]) and df['cross_price_55'][prev] == 'green':
            df['cross_price_55'][curr] = 'red'

        # ---------------------------PRICE CROSS EMA 200------------------------
        if df['close'][curr] > df['ema_200'][curr] and (df['cross_price_200'][prev] == 'red'):
            df['cross_price_200'][curr] = 'green'

        if (df['close'][curr] <= df['ema_200'][curr]) and (df['cross_price_200'][prev] == 'green'):
            df['cross_price_200'][curr] = 'red'

        # ---------------------------SUPERTREND------------------------
        if df['close'][curr] > df['supertrend'][curr]:
            df['sup_signal'][curr] = 'green'

        if df['close'][curr] <= df['supertrend'][curr]:
            df['sup_signal'][curr] = 'red'


################################## Final Decision##########################################
    # df['Final_Signal'] = 'No Signal'
    n = 10

    for curr in range(n, len(df)):
        prev = (curr - 1)

       # 1. EVENT :  #===============WHEN SUPERTREND SIGNAL CHANGED TO GREEN=======================

        if (df['sup_signal'][curr] == 'green') and (df['sup_signal'][prev] == 'red'):
            if df['cross_price_9'][curr] == 'green':
                df['final_signal'][curr] = 'buy'
                df['event'][curr] = 'WHEN SUPERTREND SIGNAL CHANGED TO GREEN'

       # 2. EVENT :  #===============WHEN SUPERTREND SIGNAL CHANGED TO RED=======================

        if (df['sup_signal'][curr] == 'red') and (df['sup_signal'][prev] == 'green'):
            if df['cross_price_9'][curr] == 'red':
                df['final_signal'][curr] = 'sell'
                df['event'][curr] = 'WHEN SUPERTREND SIGNAL CHANGED TO RED'

       # 3. EVENT :  #===============WHEN EMA9 CROSSED EMA21=======================

        if (df['cross_9_21'][curr] == 'green') and (df['cross_9_21'][prev] == 'red'):
            if df['sup_signal'][curr] == 'green':
                df['final_signal'][curr] = 'buy'
                df['event'][curr] = 'WHEN EMA9 CROSSED EMA21 TO GREEN'

        if df['cross_9_21'][curr] == 'red' and df['cross_9_21'][prev] == 'green':
            if df['sup_signal'][curr] == 'red':
                df['final_signal'][curr] = 'sell'
                df['event'][curr] = 'WHEN EMA9 CROSSED EMA21 TO RED'

       # 4. EVENT :  #===============WHEN EMA21 CROSSED EMA55=======================

        if (df['cross_21_55'][curr] == 'green') and df['cross_21_55'][prev] == 'red':
            if (df['sup_signal'][curr] == 'green') and (df['cross_9_21'][curr] == 'green'):
                df['final_signal'][curr] = 'buy'
                df['event'][curr] = 'WHEN EMA21 CROSSED EMA55 TO GREEN'

        if (df['cross_21_55'][curr] == 'red') and (df['cross_21_55'][prev] == 'green'):
            if (df['sup_signal'][curr] == 'red') and (df['cross_9_21'][curr] == 'red'):
                df['final_signal'][curr] = 'sell'
                df['event'][curr] = 'WHEN EMA21 CROSSED EMA55 TO RED'

       # 5. EVENT :  #===============WHEN PRICE CROSSED EMA55=======================

        if (df['cross_price_55'][prev] == 'green') and (df['close'][curr] > df['high'][prev]):
            if (df['sup_signal'][curr] == 'green') and (df['cross_9_21'][curr] == 'green'):
                df['final_signal'][curr] = 'buy'
                df['event'][curr] = 'WHEN PRICE CROSSED EMA55 TO GREEN'

        if (df['cross_price_55'][prev] == 'red') and (df['close'][curr] < df['low'][prev]):
            if df['sup_signal'][curr] == 'red' and df['cross_9_21'][curr] == 'red':
                df['final_signal'][curr] = 'sell'
                df['event'][curr] = 'WHEN PRICE CROSSED EMA55 TO RED'

       # 6. EVENT :  #===============WHEN PRICE CROSSED EMA200=======================

        if (df['cross_price_200'][prev] == 'green') and (df['close'][curr] > df['high'][prev]):
            if (df['sup_signal'][curr] == 'green') and (df['cross_9_21'][curr] == 'green'):
                df['final_signal'][curr] = 'buy'
                df['event'][curr] = 'WHEN PRICE CROSSED EMA200 TO GREEN'

        if (df['cross_price_200'][prev] == 'red') and (df['close'][curr] < df['low'][prev]):
            if (df['sup_signal'][curr] == 'red') and (df['cross_9_21'][curr] == 'red'):
                df['final_signal'][curr] = 'sell'
                df['event'][curr] = 'WHEN PRICE CROSSED EMA200 TO RED'

    return df
    # return df
