import datetime
from datetime import timedelta
import pandas_market_calendars as mcal
from sqlalchemy.exc import ProgrammingError, OperationalError

from myFirstDjangoSite.settings import connection


class Stocks:
    superStars = None
    superStarsQuery = None
    spy5DaysQuery = None
    risingStars = None
    risingStarsQuery = None
    spyWinners = None
    spyWinnersQuery = None
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

    def getRisingStars(self):
        result = connection.execute(self.risingStarsQuery)

        for row in result.fetchall():
            print('The data of the row is: ' + str(row))
            stock = Stock()
            stock.ticker = row['day1_ticker']
            stock.performance = [row['day5_performance'], row['day4_performance'], row['day3_performance'],
                                 row['day2_performance'], row['day1_performance']]
            stock.times = [str(row['day5_date'].date()), str(row['day4_date'].date()), str(row['day3_date'].date()),
                           str(row['day2_date'].date()), str(row['day1_date'].date())]
            self.risingStars.append(stock)

        self.risingStars.append(self.spy5DaysStock)

        return self.risingStars

    def getSPYWinners(self):
        result = connection.execute(self.spyWinnersQuery)

        for row in result.fetchall():
            print('The data of the row is: ' + str(row))
            stock = Stock()
            stock.ticker = row['day1_ticker']
            stock.performance = [row['day5_performance'], row['day4_performance'], row['day3_performance'],
                                 row['day2_performance'], row['day1_performance']]
            stock.times = [str(row['day5_date'].date()), str(row['day4_date'].date()), str(row['day3_date'].date()),
                           str(row['day2_date'].date()), str(row['day1_date'].date())]
            self.spyWinners.append(stock)

        self.spyWinners.append(self.spy5DaysStock)

        return self.spyWinners

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
        self.risingStarsQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as " \
                               "day1_performance," \
                               "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                               "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance, " \
                               "day4.Date as day4_date,  day4.Ticker as day4_ticker, day4.Performance as day4_performance, " \
                               "day5.Date as day5_date,  day5.Ticker as day5_ticker, day5.Performance as day5_performance " \
                               "from  " + self.daysBefore[0] + " as day1 inner join " + self.daysBefore[1] + " day2 " \
                                "on day1.Ticker = day2.Ticker and day1.Performance > day2.Performance " \
                                "inner join  " + self.daysBefore[2] + " as day3 on day2.Ticker = day3.Ticker and " \
                                "day2.Performance > day3.Performance inner join  " + self.daysBefore[3] + " as day4 " \
                                "on day3.Ticker = day4.Ticker and day3.Performance > day4.Performance inner join  " + self.daysBefore[4] + \
                               " as day5 on day4.Ticker = day5.Ticker and day4.Performance > day5.Performance;" \

        print(self.risingStarsQuery)

    def setSPYWinnersQuery(self):
        self.spyWinnersQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as day1_performance," \
                                "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                                "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance, " \
                                "day4.Date as day4_date,  day4.Ticker as day4_ticker, day4.Performance as day4_performance, " \
                                "day5.Date as day5_date,  day5.Ticker as day5_ticker, day5.Performance as day5_performance " \
                                "from  " + self.daysBefore[0] + " as day1 " \
                                "inner join " + self.daysBefore[1] + " day2 on day1.Ticker = day2.Ticker and " \
                                "day1.Performance >  (select Performance from " + self.daysBefore[0] + " where Ticker = 'SPY') and " \
                                "day2.Performance > (select Performance from " + self.daysBefore[1] + " where Ticker = 'SPY') " \
                                "inner join  " + self.daysBefore[2] + " as day3 on day2.Ticker = day3.Ticker and " \
                                "day3.Performance > (select Performance from " + self.daysBefore[2] + " where Ticker = 'SPY') " \
                                " inner join  " + self.daysBefore[3] + " as day4 on day3.Ticker = day4.Ticker and " \
                                "day4.Performance > (select Performance from " + self.daysBefore[3] + " where Ticker = 'SPY') " \
                                "inner join  " + self.daysBefore[4] + " as day5 on day4.Ticker = day5.Ticker and " \
                                "day5.Performance > (select Performance from " + self.daysBefore[4] + " where Ticker = 'SPY');"

        print(self.spyWinnersQuery)

    def setEverGreenQuery(self):
        self.everGreenQuery = None

    def setDaysBefore(self):
        self.daysBefore = []

        today = datetime.date.today()
        past_date = datetime.date.today() - timedelta(days=31)

        nyse = mcal.get_calendar('NYSE')
        market_days = nyse.valid_days(start_date=past_date, end_date=today)

        for market_day in reversed(market_days):
            table_name = 'snp_performance_' + str(market_day.date()).replace('-', '_')

            if self.checkTableExists(table_name):
                self.daysBefore.append(table_name)
                # print(self.daysBefore[x])

    def checkTableExists(self, table_name):
        print(table_name)
        checkQuery = 'select * from ' + table_name

        # MySQLdb._exceptions.OperationalError
        # 2013, 'Lost connection to MySQL server during query')  # 012[SQL: select * from snp_performance_2023_01_19

        try:
            connection.execute(checkQuery)
            return True
        except ProgrammingError:
            print('The table does not exist. ')
            return False
        except OperationalError as oe:
            print('OperationalError ' + str(oe))
            return self.checkTableExists(table_name)
        except Exception as e:
            print('Printing generic exception: ' + str(e))
            return False

    def __init__(self):
        self.superStars = []
        self.risingStars = []
        self.everGreen = []
        self.spyWinners = []
        self.setDaysBefore()
        self.setSPY5DaysQuery()
        self.setSPYStock()
        self.setSuperStarsQuery()
        self.setRisingStarsQuery()
        self.setSPYWinnersQuery()
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

# SPY Winners -->
# select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as day1_performance,day2.Date as day2_date,
# day2.Ticker as day2_ticker, day2.Performance as day2_performance,day3.Date as day3_date,  day3.Ticker as day3_ticker,
# day3.Performance as day3_performance, day4.Date as day4_date,  day4.Ticker as day4_ticker, day4.Performance as day4_performance,
# day5.Date as day5_date,  day5.Ticker as day5_ticker, day5.Performance as day5_performance from  snp_performance_2023_01_20 as day1
# inner join snp_performance_2023_01_18 day2 on day1.Ticker = day2.Ticker
# and day1.Performance >  (select Performance from snp_performance_2023_01_20 where Ticker = 'SPY')
# and day2.Performance > (select Performance from snp_performance_2023_01_18 where Ticker = 'SPY')
# inner join  snp_performance_2023_01_17 as day3 on day2.Ticker = day3.Ticker
# and day3.Performance > (select Performance from snp_performance_2023_01_17 where Ticker = 'SPY')
# inner join  snp_performance_2023_01_13 as day4 on day3.Ticker = day4.Ticker
# and day4.Performance > (select Performance from snp_performance_2023_01_13 where Ticker = 'SPY')
# inner join  snp_performance_2023_01_12 as day5 on day4.Ticker = day5.Ticker
# and day5.Performance > (select Performance from snp_performance_2023_01_12 where Ticker = 'SPY');

