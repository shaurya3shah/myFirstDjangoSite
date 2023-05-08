import pandas as pd
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot

df = read_csv('Traffic_Crashes_-_Vehicles.csv')
# df = read_csv('CTA_-_Ridership_-_Daily_Boarding_Totals_sample.csv')
# df['twice_total'] = df['total_rides']*2
# print(df)

df['year'] = pd.DatetimeIndex(df['CRASH_DATE']).year
df['month'] = pd.DatetimeIndex(df['CRASH_DATE']).month

# print(df)

df2 = df.groupby(['year', 'month'])['CRASH_RECORD_ID'].count().reset_index()
# print(df2)

df2.to_csv('Traffic_Crashes_Monthly.csv')



