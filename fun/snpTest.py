import unittest
import pandas as pd
import lxml
import yfinance as yf


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

        # full_performance_data1 = self.getPerformance(str(tickers[0]))
        # frames.append(full_performance_data1)
        # full_performance_data2 = self.getPerformance(str(tickers[1]))
        # frames.append(full_performance_data2)

        for ticker in tickers:
            performance_data = self.getPerformance(ticker)
            frames.append(performance_data)

        result = pd.concat(frames)

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None, 'expand_frame_repr', False):  # more options can be specified also
            print(result.sort_values(by='Performance', ascending=False))

        self.assertEqual(True, True)  # add assertion here

    def getPerformance(self, ticker):
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


if __name__ == '__main__':
    unittest.main()
