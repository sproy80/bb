import yfinance
import pandas as pd


def get_history(symbol, period='1mo', interval='15m'):

    symbol = symbol + '.NS'
    sdata = yfinance.Ticker(ticker=symbol).history(
        period=period, interval=interval)
    df = pd.DataFrame(sdata)

    df.to_csv(f'{symbol}.csv')

    dff = pd.read_csv(f'{symbol}.csv', usecols=[
                      'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # To make columns in Lower case
    dff.columns = dff.columns.str.lower()

    # Rename column name
    dff.rename(columns={'datetime': 'date'}, inplace=True)
    return dff
