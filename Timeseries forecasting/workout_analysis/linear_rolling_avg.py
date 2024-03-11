import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from load_data import load
from statsmodels.tsa.deterministic import DeterministicProcess
from statsmodels.graphics.tsaplots import plot_acf
import numpy as np

dfv = load(path='data.csv')
dates = dfv.loc[:, 'date']

dfo = load(path='onerepmax.csv')

# Do a linear correlation between the one rep max of benchpress, the volume of benchpress, and the volume of squats
# squats_volume = dfv['Squats']
# benchpress_volume = dfv['Benchpress']
target_name = 'Benchpress'
target_name2 = 'Dumbell incline press 30 degrees'
target = dfo[target_name]
target2 = dfo[target_name2]

interpolated_target = dfo['orm_interpolated'] = target.replace(0, method='pad')
interpolated_target2 = dfo['orm_interpolated2'] = target2.replace(0, method='pad')

# create a rolling average of the ORM over time
rolling_avg = interpolated_target.rolling(window=30, min_periods=14, center=False).mean()
rolling_avg.fillna(0, inplace=True)
rolling_avg2 = interpolated_target2.rolling(window=30, min_periods=14, center=False).mean()
rolling_avg2.fillna(0, inplace=True)

# Plot autocorrelation of the target to determine lags
# plot_acf(target, lags=40)
# plt.show()

# Workout day feature
dfo['workout_day'] = (dfv['weightVolume'] > 0).astype(int)

# Create a linear regression model
dp = DeterministicProcess(
    index=dfo.index,  # dates from the training data
    constant=False,       # dummy feature for the bias (y_intercept)
    order=1,           # the time dummy (trend) polynomial order.
    drop=True,           # drop terms if necessary to avoid collinearity
)
# Create a linear regression model
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=60)
model = LinearRegression()

y = interpolated_target

model.fit(X, y)
y_pred = pd.Series(model.predict(X), index=X.index)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

dp2 = DeterministicProcess(
    index=dfo.index,  # dates from the training data
    constant=False,       # dummy feature for the bias (y_intercept)
    order=1,           # the time dummy (trend) polynomial order.
    drop=True,           # drop terms if necessary to avoid collinearity
)
X2 = dp2.in_sample()
X_fore2 = dp.out_of_sample(steps=60)
# remove the days where the ORM is 0
target2 = target2[interpolated_target2 > 0]
X2 = X2[interpolated_target2 > 0]
dates2 = dates[interpolated_target2 > 0]

y = interpolated_target2
# remove the days where the ORM is 0
y = y[interpolated_target2 > 0]
model.fit(X2, y)
y_pred2 = pd.Series(model.predict(X2), index=X2.index)
y_fore2 = pd.Series(model.predict(X_fore), index=X_fore.index)

# create a new pd.Series with dates for the next 30 days
forecasted_dates = pd.date_range(start=dates.max(), periods=60, freq='D')
# Plot 4 subplots each with a different target
fig, ax = plt.subplots(1, 2)
ax[0].scatter(dfo['date'], target, color='grey', label=f'{target_name} ORM')
ax[0].plot(dfo['date'], y_pred, color='blue', label='Trend')
ax[0].plot(dfo['date'], rolling_avg, color='black', label='Rolling average')
ax[0].plot(forecasted_dates, y_fore, color='green', label='Future Trend')
ax[0].set_title(f'{target_name} ORM')
ax[0].set_xlabel('Date')
ax[0].set_ylabel('ORM')
ax[0].legend()
ax[1].bar(dates2, target2, color='black', label=f'{target_name2} ORM')
ax[1].plot(dates2, y_pred2, color='blue', label='Trend')
#ax[1].plot(dates2, rolling_avg2, color='black', label='Rolling average')
ax[1].plot(forecasted_dates, y_fore2, color='green', label='Future Trend')
ax[1].set_title(f'{target_name2} ORM')
ax[1].set_xlabel('Date')
ax[1].set_ylabel('ORM')
ax[1].legend()

plt.show()




















