from myFirstDjangoSite.settings import connection


class Stocks:
    superStars = None
    superStarsQuery = None
    spyQuery = None
    risingStars = None
    risingStarsQuery = None
    everGreen = None
    everGreenQuery = None
    spyStock = None

    def getSuperStars(self):
        result = connection.execute(self.superStarsQuery)

        for row in result.fetchall():
            print(row)
            stock = Stock()
            stock.ticker = row['day1_ticker']
            stock.performance = [row['day1_performance'], row['day2_performance'], row['day3_performance']]
            stock.times = [str(row['day1_date'].date()), str(row['day2_date'].date()), str(row['day3_date'].date())]
            self.superStars.append(stock)

        self.superStars.append(self.spyStock)

        return self.superStars

    def setSPYQuery(self):
        self.spyQuery = "select Date, Ticker, Performance from snp_performance_2023_01_11 where Ticker = " \
                        "'SPY' union select Date, Ticker, Performance from snp_performance_2023_01_12 where " \
                        "Ticker = 'SPY' union select Date, Ticker, Performance from " \
                        "snp_performance_2023_01_13 where Ticker = 'SPY' order by Date asc; "

    def setSPYStock(self):
        result = connection.execute(self.spyQuery)

        self.spyStock = Stock()
        for row in result.fetchall():
            print(row)
            self.spyStock.ticker = row['Ticker'] + ' for Reference'
            self.spyStock.performance.append(row['Performance'])
            self.spyStock.times.append(str(row['Date'].date()))

    def setSuperStarsQuery(self):
        self.superStarsQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as " \
                               "day1_performance," \
                               "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                               "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance " \
                               "from  snp_performance_2023_01_11 as day1 inner join snp_performance_2023_01_12 day2 " \
                               "on day1.Ticker = day2.Ticker and day1.Performance > 3 and day2.Performance > 3 " \
                               "inner join snp_performance_2023_01_13 as day3 on day2.Ticker = day3.Ticker and " \
                               "day3.Performance > 3; "

    def setRisingStarsQuery(self):
        self.risingStarsQuery = None

    def setEverGreenQuery(self):
        self.everGreenQuery = None

    def __init__(self):
        self.superStars = []
        self.risingStars = []
        self.everGreen = []
        self.setSPYQuery()
        self.setSPYStock()
        self.setSuperStarsQuery()
        self.setRisingStarsQuery()
        self.setEverGreenQuery()


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
