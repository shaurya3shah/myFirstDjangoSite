import datetime
from datetime import timedelta

from sqlalchemy.exc import ProgrammingError

from myFirstDjangoSite.settings import connection


class Stocks:
    superStars = None
    superStarsQuery = None
    spy5DaysQuery = None
    risingStars = None
    risingStarsQuery = None
    everGreen = None
    everGreenQuery = None
    spy5DaysStock = None
    daysBefore = []

    def getSuperStars(self):
        result = connection.execute(self.superStarsQuery)

        for row in result.fetchall():
            print('The data of the row is: ' + str(row))
            stock = Stock()
            stock.ticker = row['day1_ticker']
            stock.performance = [row['day5_performance'], row['day4_performance'], row['day3_performance'],
                                 row['day2_performance'], row['day1_performance']]
            stock.times = [str(row['day5_date'].date()), str(row['day4_date'].date()), str(row['day3_date'].date()),
                           str(row['day2_date'].date()), str(row['day1_date'].date())]
            self.superStars.append(stock)

        self.superStars.append(self.spy5DaysStock)

        return self.superStars

    def setSPY5DaysQuery(self):
        self.spy5DaysQuery = "select Date, Ticker, Performance from " + self.daysBefore[0] + "  where Ticker = 'SPY' " \
                        "union all select Date, Ticker, Performance from " + self.daysBefore[1] + " where Ticker = 'SPY' " \
                        "union all select Date, Ticker, Performance from " + self.daysBefore[2] + " where Ticker = 'SPY' " \
                        "union all select Date, Ticker, Performance from " + self.daysBefore[3] + " where Ticker = 'SPY' " \
                        "union all select Date, Ticker, Performance from " + self.daysBefore[4] + " where Ticker = 'SPY' " \
                        "order by Date asc; "

        print(self.spy5DaysQuery)

    def setSPYStock(self):
        result = connection.execute(self.spy5DaysQuery)

        self.spy5DaysStock = Stock()
        for row in result.fetchall():
            print(row)
            self.spy5DaysStock.ticker = row['Ticker'] + ' for Reference'
            self.spy5DaysStock.performance.append(row['Performance'])
            self.spy5DaysStock.times.append(str(row['Date'].date()))

    def setSuperStarsQuery(self):
        self.superStarsQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as " \
                               "day1_performance," \
                               "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                               "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance, " \
                               "day4.Date as day4_date,  day4.Ticker as day4_ticker, day4.Performance as day4_performance, " \
                               "day5.Date as day5_date,  day5.Ticker as day5_ticker, day5.Performance as day5_performance " \
                               "from  " + self.daysBefore[0] + " as day1 inner join " + self.daysBefore[1] + " day2 " \
                                "on day1.Ticker = day2.Ticker and day1.Performance > 0 and day2.Performance > 0 " \
                                "inner join  " + self.daysBefore[2] + " as day3 on day2.Ticker = day3.Ticker and " \
                                "day3.Performance > 0 inner join  " + self.daysBefore[3] + " as day4 " \
                                "on day3.Ticker = day4.Ticker and day4.Performance > 0 inner join  " + self.daysBefore[4] + \
                               " as day5 on day4.Ticker = day5.Ticker and day5.Performance > 0;" \

        print(self.superStarsQuery)

    def setRisingStarsQuery(self):
        self.risingStarsQuery = None

    def setEverGreenQuery(self):
        self.everGreenQuery = None

    def setDaysBefore(self):
        self.daysBefore = []

        minus_a_day = 1

        if self.checkTodaysTableExists():
            minus_a_day = 0

        for x in range(31):
            date_part = ''

            if (datetime.date.today() - timedelta(days=x + minus_a_day)).isoweekday() < 6:
                date_part = str(datetime.date.today() - timedelta(days=x + minus_a_day)).replace('-', '_')
                table_name = 'snp_performance_' + date_part
                self.daysBefore.append(table_name)
                # print(self.daysBefore[x])

    def checkTodaysTableExists(self):
        table_name = 'snp_performance_' + str(datetime.date.today()).replace('-', '_')
        print(table_name)
        checkQuery = 'select * from ' + table_name

        try:
            connection.execute(checkQuery)
        except ProgrammingError:
            print('The table does not exist. ')
            return False
        except Exception as e:
            print('Printing generic exception: ' + str(e))
            return True

    def __init__(self):
        self.superStars = []
        self.risingStars = []
        self.everGreen = []
        self.setDaysBefore()
        self.setSPY5DaysQuery()
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
