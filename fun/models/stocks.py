class Stocks:
    superStars = None
    risingStars = None
    everGreen = None

    def getSuperStars(self):
        self.superStars = StockCollection()
        spy = Stock()
        spy.ticker = 'SPY'
        spy.performance = [1, 3, 5]

        self.superStars.collection.append(spy)
        self.superStars.tickers.append(spy.ticker)

        ual = Stock()
        ual.ticker = 'UAL'
        ual.performance = [4, 5, 6]

        self.superStars.collection.append(ual)
        self.superStars.tickers.append(ual.ticker)

        return self.superStars

    def __init__(self):
        self.superStars = []
        self.risingStars = []
        self.everGreen = []


class Stock:
    ticker = None
    performance = []

    def __init__(self):
        self.ticker = None
        self.performance = []


class StockCollection:
    collection = []
    tickers = []
