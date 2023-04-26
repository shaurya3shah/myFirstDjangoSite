# evaluate an ARIMA model using a walk-forward validation
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# https://www.transitchicago.com/meetingthemoment/scorecard/
# load dataset

monthly_series = read_csv('CTA_Ridership2023.csv', header=0, index_col=0, parse_dates=True)
monthly_series.index = monthly_series.index.to_period('M')
monthly_x = monthly_series.values

model = ARIMA(monthly_x, order=(0, 0, 5))
model_fit = model.fit()
output = model_fit.forecast(6)

print(output)

# pyplot.plot(monthly_x)
# pyplot.show()
# pyplot.plot(output)
# pyplot.show()
#
# [19379780.39059499 20598945.88027454 21322522.12437582 22212405.62217901 22147609.97051312 22694007.02000006]
