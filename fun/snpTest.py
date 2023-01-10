import unittest
import pandas as pd
import lxml
import yfinance as yf


class RobotFinance(unittest.TestCase):
    def test_snp_500(self):
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
        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers="SPY AAPL MSFT",

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period="ytd",

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

        print(data)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
