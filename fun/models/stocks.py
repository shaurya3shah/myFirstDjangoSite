class Stocks:
    superStars = None
    risingStars = None
    everGreen = None

    def getSuperStars(self):
        spy = Stock()
        spy.ticker = 'SPY'
        spy.performance = [1, 3, 5]
        spy.times = "['Jan 11', 'Jan 12', 'Jan 13']"

        self.superStars.append(spy)

        ual = Stock()
        ual.ticker = 'UAL'
        ual.performance = [4, 5, 6]
        ual.times = "['Jan 11', 'Jan 12', 'Jan 13']"

        self.superStars.append(ual)

        return self.superStars

    def __init__(self):
        self.superStars = []
        self.risingStars = []
        self.everGreen = []


class Stock:
    ticker = None
    performance = []
    times = []

    def __init__(self):
        self.ticker = None
        self.performance = []
        self.times = []
