from datetime import date, timedelta, time, datetime
import time
from fyers_bot import history as fyersHistory
from strategies import superEma
import pandas as pd
from bb_logging import write_log, write_error_log
from manager_db import add_to_signals
import provider as dataProvider

# symbol = 'CRUDEOIL23APRFUT'
# exchange = 'MCX'
# time_frame = '15'

# DATE FORMAT : 2023-03-22 - YYYY-MM-DD


class Trade():

    def __init__(self, provider: dataProvider.data_provider,
                 symbol, exchange, time_frame,
                 lookback=1, target=20, stoploss=20, price_tolerance=5.00, period='', sleep=0) -> None:
        self.provider = provider
        self.symbol = symbol
        self.exchange = exchange
        self.time_frame = time_frame
        self.lookback = lookback
        self.isActiveBuyTrade = False
        self.isActiveSellTrade = False
        self.target = target
        self.stoploss = stoploss
        self.entry_price = 0.00
        self.price_tolearnce = price_tolerance
        self.period = period
        self.sleep = sleep

    tradeReason = ""

    @property
    def isActiveBuyTrade(self) -> bool:
        return self._isActiveBuyTrade

    @isActiveBuyTrade.setter
    def isActiveBuyTrade(self, value: bool) -> bool:
        self._isActiveBuyTrade = value

    @property
    def isActiveSellTrade(self) -> bool:
        return self._isActiveSellTrade

    @isActiveSellTrade.setter
    def isActiveSellTrade(self, value: bool) -> bool:
        self._isActiveSellTrade = value

    @property
    def range_form(self) -> str:
        return str(date.today() - timedelta(days=self.lookback))

    @property
    def range_to(self) -> str:
        return str(date.today())

    @property
    def entry_price(self) -> float:
        return self._entry_price

    @entry_price.setter
    def entry_price(self, value) -> float:
        self._entry_price = value

    def main(self):

        print(f"\n Bot Started at {datetime.now()} \n")
        ########################################################

        # df = fyersHistory.get_historical_data(
        #     symbol=self.symbol, exchange=self.exchange, resolution=self.time_frame, range_form=self.range_form, range_to=self.range_to)

        df = dataProvider.get_data(provider=self.provider, symbol=self.symbol, exchange=self.exchange,
                                   period=self.period, time_frame=self.time_frame, range_from=self.range_form, range_to=self.range_to)

        if (self.isActiveBuyTrade or self.isActiveSellTrade):
            signal = self.chk_for_exit(df)
        else:
            signal = self.chk_for_entry(df)

    def chk_for_exit(self, df):
        global tradeReason
        result = 'No Signal'
        dff = superEma.trade_decision(df)
        decision = dff.tail(1)
        print(str(dff.tail(3)))
        price = decision['close'].values[0]

        if self. isExit(dff):
            self.entry_price = 0.00
            if (self.isActiveSellTrade == True):
                msg = str(datetime.now(
                )) + '====================Exit Sell Trade=================================' + '\n'
                msg += str(decision)
                write_log(f"{self.symbol}_log.txt", msg)
                result = 'exit sell'
                self.isActiveSellTrade = False
                add_to_signals(symbol=self.symbol,
                               price=price, signal_type=result,
                               time_frame=self.time_frame,
                               reason=tradeReason)

            if (self.isActiveBuyTrade == True):
                msg = str(datetime.now(
                )) + '====================Exit Buy Trade=================================' + '\n'
                msg += str(decision)
                write_log(f"{self.symbol}_log.txt", msg)
                result = 'exit buy'

                self.isActiveBuyTrade = False
                add_to_signals(symbol=self.symbol,
                               price=price, signal_type=result,
                               time_frame=self.time_frame,
                               reason=tradeReason)

        return result

    def chk_for_entry(self, df):
        global tradeReason
        result = 'No Signal'
        dff = superEma.trade_decision(df)

        # dff = check_for_existing_signals(dff)

        decision = dff.tail(1)
        print(str(dff.tail(3)))
        price = decision['close'].values[0]

        if (decision['Final_Signal'].values == 'Sure Buy' and self.isActiveBuyTrade == False and self.isActiveSellTrade == False) and self.isEntry(dff):
            msg = str(datetime.now(
            )) + '====================Buy Order=================================' + '\n'
            msg += str(decision)
            write_log(f"{self.symbol}_log.txt", msg)
            result = 'buy'
            self.isActiveBuyTrade = True
            self.entry_price = price
            tradeReason = 'buy'
            add_to_signals(symbol=self.symbol,
                           price=price, signal_type=result,
                           time_frame=self.time_frame,
                           reason=tradeReason)

        if (decision['Final_Signal'].values == 'Sure Sell' and self.isActiveBuyTrade == False and self.isActiveSellTrade == False) and self.isEntry(dff):
            msg = str(datetime.now(
            )) + '====================Sell Order=================================' + '\n'
            msg += str(decision)
            write_log(f"{self.symbol}_log.txt", msg)
            result = 'sell'
            self.isActiveSellTrade = True
            self.entry_price = price
            tradeReason = 'sell'
            add_to_signals(symbol=self.symbol,
                           price=price, signal_type=result,
                           time_frame=self.time_frame,
                           reason=tradeReason)

        return result

    def run_bot(self):

        while True:
            try:
                self.main()
            except Exception as ex:
                print(f'Error Occured...{ex}')
                write_error_log(f"{self.symbol}_error.txt",
                                f"Error Time : {datetime.now()} \n Error Details : {ex} \n")

            print("\n")
            print(f"Active Buy Trade :- {self.isActiveBuyTrade}")
            print(f"Active Sell Trade :- {self.isActiveSellTrade}")
            print(f'\n\n{self.symbol} Bot is running ...')
            print("=" * 80)
            time.sleep(self.sleep)

    def isEntry(self, df) -> bool:
        global tradeReason
        curr_bar = df.iloc[len(df) - 1]
        prev_bar = df.iloc[len(df) - 2]
        curr_price = curr_bar.close
        curr_Ema9 = curr_bar.EMA_9
        curr_Ema21 = curr_bar.EMA_21
        curr_Ema55 = curr_bar.EMA_55
        curr_Ema200 = curr_bar.EMA_200
        curr_supertrend = curr_bar.Supertrend

        isPriceAboveEma55 = (curr_price > curr_Ema55)
        isPriceAboveEma200 = (curr_price > curr_Ema200)

        if curr_bar.Final_Signal == 'Sure Buy':

            # EMA55 OR EMA200 if just above price then we should check whether these lines comes between price and target
            entry_condition = False
            isPriceNearEma9 = self.chk_price_near_ema9(
                curr_bar, prev_bar, isBuy=True)

            if isPriceNearEma9:

                if (not isPriceAboveEma55 and (curr_Ema55 - curr_price < self.target)):
                    print("Target not achievable for EMA55")
                    return False

                if (not isPriceAboveEma200 and (curr_Ema200 - curr_price < self.target)):
                    print("Target not achievable for EMA200")
                    return False
            else:
                return False

        if curr_bar.Final_Signal == 'Sure Sell':

            # EMA55 OR EMA200 if just below price then we should check whether these lines comes between price and target

            isPriceNearEma9 = self.chk_price_near_ema9(
                curr_bar, prev_bar, isBuy=False)

            if isPriceNearEma9:
                if (isPriceAboveEma55 and (curr_price - curr_Ema55 < self.target)):
                    print("Target not achievable for EMA55")
                    return False

                if (isPriceAboveEma200 and (curr_price - curr_Ema200 < self.target)):
                    print("Target not achievable for EMA200")
                    return False

            else:
                print("Price not near")
                return False

        return True

    def chk_price_near_ema9(self, curr_bar, prev_bar, isBuy=True):
        close = curr_bar.close
        open = curr_bar.open
        high = curr_bar.high
        low = curr_bar.low

        # Trade only price near EMA9
        print(f"isBuy  : {isBuy}")

        print(f"EMA_9 : {curr_bar.EMA_9}")

        buyCondition = (curr_bar.close > prev_bar.high) and (
            (curr_bar.close - curr_bar.EMA_9) < self.price_tolearnce)

        sellCondition = (curr_bar.close < prev_bar.low) and (
            (curr_bar.EMA_9 - curr_bar.close) < self.price_tolearnce)

        print(
            f"Condition Buy : {buyCondition}")

        print(
            f"Condition Sell : {sellCondition}")

        if isBuy and buyCondition:
            return True

        if not isBuy and sellCondition:
            return True
        else:

            print(
                "Price is not near to EMA-9 or geater/less than high/close of prev candle")

        return False

    def isExit(self, df) -> bool:

        global tradeReason
        curr_bar = df.iloc[len(df) - 1]
        prev_bar = df.iloc[len(df) - 2]
        curr_price = curr_bar.close
        curr_Ema9 = curr_bar.EMA_9
        curr_Ema21 = curr_bar.EMA_21
        curr_Ema55 = curr_bar.EMA_55
        curr_Ema200 = curr_bar.EMA_200
        curr_supertrend = curr_bar.Supertrend

        isPriceAboveEma55 = (curr_price > curr_Ema55)
        isPriceAboveEma200 = (curr_price > curr_Ema200)

        # 1. If currenct price => Target price for buy
        if ((curr_price - self.entry_price) >= self.target) and self.isActiveBuyTrade:
            tradeReason = "currenct price => Target price for buy"
            return True

            # 1.1 If currenct price => Target price for sell
        if ((self.entry_price - curr_price) >= self.target) and self.isActiveSellTrade:
            tradeReason = "currenct price => Target price for sell"
            return True

            # 2. If stoploss hit for buy
        if ((self.entry_price - curr_price) >= self.stoploss) and self.isActiveBuyTrade:
            tradeReason = "stoploss hit for buy"
            return True

            # 2.1 If stoploss hit for sell
        if ((curr_price - self.entry_price) >= self.stoploss) and self.isActiveSellTrade:
            tradeReason = "stoploss hit for sell"
            return True

            # 3. If current EMA9 < EMA21 for BUY trade
        if curr_Ema9 < curr_Ema21 and self.isActiveBuyTrade == True:
            tradeReason = "current EMA9 < EMA21 for BUY trade"
            return True

            # 4. If current EMA9 > EMA21 price for SELL trade
        if curr_Ema9 > curr_Ema21 and self.isActiveSellTrade == True:
            tradeReason = "current EMA9 > EMA21 for sell trade"
            return True

        ''' TODO : Below code will be open once supertrend calculation finalized.
            
        '''
        # #5. If current Supertrend > curr price for sell trade
        # if curr_price > curr_supertrend and self.isActiveSellTrade == True:
        #     return True

        # #6. If current Supertrend < curr price for buy trade
        # if curr_price < curr_supertrend and self.isActiveBuyTrade == True:
        #     return True

        # -------------------------------------------------Below codes not tested

        # 6. If price very near , equal to or greater than any EMA Lines
        # 6.1 If Buy

        if (self.isActiveBuyTrade and ((curr_Ema55 > self.entry_price) or (curr_Ema200 > self.entry_price))):

            if not isPriceAboveEma55 and ((curr_Ema55 - curr_price) < 1):
                tradeReason = "price very near , equal to or greater than any EMA 55"
                return True

            if not isPriceAboveEma200 and ((curr_Ema200 - curr_price) < 1):
                tradeReason = "price very near , equal to or greater than any EMA 200"
                return True

        if (self.isActiveSellTrade and ((curr_Ema55 < self.entry_price) or (curr_Ema200 < self.entry_price))):

            if isPriceAboveEma55 and ((curr_price - curr_Ema55) < 1):
                tradeReason = "price very near , equal to or greater than any EMA 55"
                return True

            if isPriceAboveEma200 and ((curr_price - curr_Ema200) < 1):
                tradeReason = "price very near , equal to or greater than any EMA 200"
                return True

        return False
