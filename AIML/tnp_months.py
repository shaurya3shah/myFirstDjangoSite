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

df = read_csv('Transportation_Network_Providers_-_Trips__Dec.csv')
# split into train and test sets
# print(df.values)


df['year'] = pd.DatetimeIndex(df['Trip Start Timestamp']).year
df['month'] = pd.DatetimeIndex(df['Trip Start Timestamp']).month

# print(df)

df2 = df.groupby(['year', 'month'])['Trip ID'].count().reset_index()
# print(df2)

df2.to_csv('tnp_ridership_months_Dec.csv')


