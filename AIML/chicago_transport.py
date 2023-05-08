import pandas as pd
from pandas import read_csv


df_cta = read_csv('cta_ridership_months.csv')
df_crashes = read_csv('Traffic_Crashes_Monthly.csv')

df_unified = pd.merge(df_cta, df_crashes, on=['month', 'year'])

df_unified['Date'] = df_unified['month'].astype(str) + '-' + df_unified['year'].astype(str)

print(df_unified[['Date', 'total_rides', 'CRASH_COUNTS']])