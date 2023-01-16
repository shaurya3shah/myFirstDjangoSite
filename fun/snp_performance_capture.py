import pandas as pd
import yfinance as yf
import sqlalchemy as db
import datetime

def getPerformance(ticker):
    # https://pypi.org/project/yfinance/
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        # tickers="SPY AAPL MSFT",
        tickers=ticker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        # period="1d",
        start="2023-01-12", end="2023-01-13",

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


# engine = db.create_engine("mysql://sns:connectdb@sns.mysql.pythonanywhere-services.com/sns$stocks")
engine = db.create_engine("mysql://root:Hello123!@localhost/stocks")
connection = engine.connect()

# table_name = 'snp_performance_' + str(datetime.date.today()).replace('-', '_')
table_name = 'snp_performance_' + str('2023-01-12').replace('-', '_')

result.to_sql(name = table_name , con = engine, if_exists = 'replace', index = True)