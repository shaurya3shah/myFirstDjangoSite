# evaluate an ARIMA model using a walk-forward validation
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# https://www.transitchicago.com/meetingthemoment/scorecard/
# load dataset

# series = read_csv('CTA_Ridership_Univariate.csv', header=0, index_col=0, parse_dates=True)
# # split into train and test sets
# X = series.values
# size = int(len(X) * 0.999)
# train, test = X[0:size], X[size:len(X)]
# history = [x for x in train]
# predictions = list()
# # walk-forward validation
# for t in range(len(test)):
#     model = ARIMA(history, order=(3, 1, 0))
#     model_fit = model.fit()
#     output = model_fit.forecast()
#     yhat = output[0]
#     predictions.append(yhat)
#     obs = test[t]
#     history.append(obs)
#     print('predicted=%f, expected=%f' % (yhat, obs))
# # evaluate forecasts
# rmse = sqrt(mean_squared_error(test, predictions))
# print('Test RMSE: %.3f' % rmse)
#
#
# series.plot()
# pyplot.show()
#
# # plot forecasts against actual outcomes
# pyplot.plot(test)
# pyplot.plot(predictions, color='red')
# pyplot.show()

monthly_series = read_csv('CTA_Ridership2023.csv', header=0, index_col=0, parse_dates=True)
monthly_series.index = monthly_series.index.to_period('M')
monthly_x = monthly_series.values

model = ARIMA(monthly_x, order=(0, 0, 2))
model_fit = model.fit()
output = model_fit.forecast(6)

print(output)

pyplot.plot(monthly_x)
pyplot.plot(output)
pyplot.show()
