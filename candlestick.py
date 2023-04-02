
class CandleColor():
    def __init__(self) -> None:
        pass

    GREEN = 'green'
    RED = 'red'
    ANY_COLOR = 'all'


class Candlestick():

    def __init__(self, open: float, high: float, low: float, close: float, fiblevel: float = 0.333) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.fiblevel = fiblevel

    def Hammer(self, colorFilter: CandleColor) -> bool:
        # Calculate fibonacci level for current candle
        bullFib = (self.low - self.high) * self.fiblevel + self.high
        bearFib = (self.high - self.low) * self.fiblevel + self.low

        # Determine which price source closes or opens highest/lowest

        if self.close < self.open:
            lowestBody = self.close
        else:
            lowestBody = self.open

        # Determine if we have a valid hammer or shooting star
        if colorFilter == 'green':
            greenCandle = lowestBody >= bullFib and self.close > self.open
            return greenCandle

        if colorFilter == 'red':
            redCandle = lowestBody >= bullFib and self.close < self.open
            return redCandle

        if colorFilter == 'all':
            allCandle = lowestBody >= bullFib and self.close > self.open
            return allCandle

    def ShootingStar(self, colorFilter: CandleColor) -> bool:
        # Calculate fibonacci level for current candle
        bullFib = (self.low - self.high) * self.fiblevel + self.high
        bearFib = (self.high - self.low) * self.fiblevel + self.low

        # Determine which price source closes or opens highest/lowest
        if self.close > self.open:
            highestBody = self.close
        else:
            highestBody = self.high

        # Determine if we have a valid hammer or shooting star
        if colorFilter == 'green':
            greenCandle = highestBody <= bearFib and self.close > self.open
            return greenCandle

        if colorFilter == 'red':
            redCandle = highestBody <= bearFib and self.close < self.open
            return redCandle

        if colorFilter == 'all':
            allCandle = highestBody <= bearFib and self.close > self.open
            return allCandle
