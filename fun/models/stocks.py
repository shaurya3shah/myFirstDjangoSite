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



# Rising Stars -->
# mysql> select * from  snp_performance_2023_01_11 as jan11 inner join snp_performance_2023_01_12 jan12 on jan11.Ticker = \
#     jan12.Ticker and jan11.Performance > 1 and jan12.Performance > 2 inner join snp_performance_2023_01_13 as jan13
# on jan12.Ticker = jan13.Ticker and jan13.Performance > 3;
#
# Super Stars -->
# select * from  snp_performance_2023_01_11 as jan11 inner join snp_performance_2023_01_12 jan12 on jan11.Ticker = jan12.Ticker
# and jan11.Performance > 3 and jan12.Performance > 3 inner join snp_performance_2023_01_13 as jan13 on jan12.Ticker = jan13.Ticker \
# and jan13.Performance > 3;