# evaluate an ARIMA model using a walk-forward validation
import pandas as pd
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# https://www.transitchicago.com/meetingthemoment/scorecard/
# load dataset

df = read_csv('CTA_-_Ridership_-_Daily_Boarding_Totals.csv')
# split into train and test sets
# print(df.values)

dates = df["service_date"]

year = list()
day = list()

for x in dates:
    # print('value is: ' + x)
    date = datetime.strptime(x, '%m/%d/%Y')
    # print(date.year)
    # print(date.strftime('%A'))
    year.append(date.year)
    day.append(date.strftime('%A'))

df['day'] = day
df['year'] = year

# print(df)
# df.to_csv('cta_ridership_days_sample_raw.csv')

df2 = df.groupby(['day','year']).sum().reset_index()
# print(df2)

df2.to_csv('cta_ridership_days.csv')

# print(df2['day'])
# print(df2['year'])
# print(df2['total_rides'])

df3 = df2.pivot_table(index='day', columns='year', values='total_rides')
df3.to_csv('cta_ridership_days_pivot.csv')



df3.plot()
pyplot.show()


