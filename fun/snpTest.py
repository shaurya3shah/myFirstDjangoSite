import datetime
from datetime import timedelta
import unittest

import pandas_market_calendars as mcal
import pandas as pd
import yfinance as yf
from sqlalchemy.exc import ProgrammingError

from myFirstDjangoSite.settings import connection



def getPerformance(ticker):
    # https://pypi.org/project/yfinance/
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        # tickers="SPY AAPL MSFT",
        tickers=ticker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period="1d",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval="1d",

        # Whether to ignore timezone when aligning ticker data from
        # different timezones. Default is True. False may be useful for
        # minute/hourly data.
        ignore_tz=False,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by='ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust=True,

        # attempt repair of missing data or currency mixups e.g. $/cents
        repair=False,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost=True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy=None
    )

    data.insert(0, 'Ticker', ticker, True)
    data.insert(6, 'Performance', ((data['Close'] - data['Open']) * 100 / data['Open']), True)

    # data['Performance'] = (data['Close'] - data['Open']) * 100 / data['Open']

    return data


class RobotFinance(unittest.TestCase):
    def test_snp_500(self):
        # https://tcoil.info
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        companies = table[0]

        # with pd.option_context('display.max_rows', None, 'display.max_columns',
        #                        None):  # more options can be specified also
        #     print(companies)

        tickers = companies['Symbol'].values.tolist()

        print('All S&P 500 Tickers: ' + str(tickers))

        print('First S&P 500 Ticker: ' + str(tickers[0]))

        self.assertEqual(True, True)  # add assertion here

    def test_ticker_msft(self):
        # https://pypi.org/project/yfinance/
        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            # tickers="SPY AAPL MSFT",
            tickers="ADM",

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            # period="1d",
            start="2023-01-11", end="2023-01-12",

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval="1d",

            # Whether to ignore timezone when aligning ticker data from
            # different timezones. Default is True. False may be useful for
            # minute/hourly data.
            ignore_tz=False,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by='ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust=True,

            # attempt repair of missing data or currency mixups e.g. $/cents
            repair=False,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost=True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads=True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy=None
        )

        # print(data.iloc[[0]])

        data.insert(5, 'Performance', [0], True)

        data['Performance'] = (data['Close'] - data['Open']) * 100 / data['Open']

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(data)

        self.assertEqual(True, True)  # add assertion here

    def test_consolidate_data(self):
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        companies = table[0]

        tickers = companies['Symbol'].values.tolist()

        frames = []

        performance_data = getPerformance('SPY')  # first add SPY
        frames.append(performance_data)

        for ticker in tickers:
            performance_data = getPerformance(ticker)
            frames.append(performance_data)

        result = pd.concat(frames).sort_values(by='Performance', ascending=False)

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None, 'expand_frame_repr', False):  # more options can be specified also
            print(result)

        # result.plot(kind='bar', x='Ticker', y='Performance')

        self.assertEqual(True, True)  # add assertion here

    # def test_get_stock_info(self):
    #     msft = yf.Ticker("MSFT")
    #     print(msft.info)
    #     # print(msft.info['regularMarketPrice'])
    #     self.assertEqual(True, True)  # add assertion here

    def test_date_name(self):
        # e = datetime.date.today()
        # print(str(e))
        # print(str(e).replace('-', '_'))
        # print(str(e.month) + '_' + str(e.day) + '_' + str(e.year))

        table_name = 'snp_performance_' + str(datetime.date.today()).replace('-', '_')

        print(table_name)

        self.assertEqual(True, True)  # add assertion here

    def test_super_stars_query(self):
        superStarQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as " \
                         "day1_performance," \
                         "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                         "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance " \
                         "from  snp_performance_2023_01_11 as day1 inner join snp_performance_2023_01_12 day2 " \
                         "on day1.Ticker = day2.Ticker and day1.Performance > 3 and day2.Performance > 3 " \
                         "inner join snp_performance_2023_01_13 as day3 on day2.Ticker = day3.Ticker and " \
                         "day3.Performance > 3; "
        result = connection.execute(superStarQuery)

        for row in result.fetchall():
            print(row)
            print(row['day1_date'])
            print(row['day1_ticker'])
            print(row['day1_performance'])
            print(row['day2_date'])
            print(row['day2_ticker'])
            print(row['day2_performance'])
            print(row['day3_date'])
            print(row['day3_ticker'])
            print(row['day3_performance'])
        self.assertEqual(True, True)  # add assertion here

    def test_days_before(self):
        daysBefore = []

        for x in range(31):
            table_name = 'snp_performance_' + str(datetime.date.today() - timedelta(days=x)).replace('-', '_')
            daysBefore.append(table_name)
            print(daysBefore[x])

        self.assertEqual(True, True)

    def test_check_table_exists(self):
        table_name = 'snp_performance_2023_01_17'
        checkQuery = 'select * from ' + table_name

        try:
            connection.execute(checkQuery)
        except ProgrammingError:
            print('The table does not exist. ')
        except Exception as e:
            print('Printing generic exception: ' + str(e))

        self.assertEqual(True, True)

    def test_check_market_day(self):
        # check valid market date = https://stackoverflow.com/questions/59360230/get-next-trading-day-using-pandas-market-calendar

        today = datetime.date.today()
        past_date = datetime.date.today() - timedelta(days=31)

        nyse = mcal.get_calendar('NYSE')
        market_days = nyse.valid_days(start_date=past_date, end_date=today)

        for market_day in reversed(market_days):
            print(market_day.date())

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()

# storing data: https://stackoverflow.com/questions/64773557/load-a-pandas-table-to-dynamodb
