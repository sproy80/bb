import pandas as pd
from datetime import datetime


df = pd.DataFrame()


def tr(df):
    df['prev_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc'] = df['high'] - df['prev_close']
    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr


def atr(df, period=10):
    df['tr'] = tr(df)
    my_atr = df['tr'].rolling(period).mean()
    return my_atr


def supertrend(df, period, multiplier=3.0):
    df['atr'] = atr(df, period=period)
    df['basic_upperband'] = ((df['high'] + df['low']) /
                             2) + (multiplier * df['atr'])
    df['basic_upperband'] = ((df['high'] + df['low']) /
                             2) - (multiplier * df['atr'])

    return df
