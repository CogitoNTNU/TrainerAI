import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from load_data import load
from statsmodels.tsa.deterministic import DeterministicProcess
from statsmodels.graphics.tsaplots import plot_acf
import numpy as np
import boostedHybrid as bh
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import RegressorChain
from sklearn.model_selection import train_test_split

def make_lags(ts, lags, lead_time=1):
    return pd.concat(
        {
            f'y_lag_{i}': ts.shift(i)
            for i in range(lead_time, lags + lead_time)
        },
        axis=1)

def make_multistep_target(ts, steps):
    return pd.concat(
        {f'y_step_{i + 1}': ts.shift(-i)
         for i in range(steps)},
        axis=1)


# Load data
dfv = load(path='data.csv')
dfo = load(path='onerepmax.csv')
dates = dfv.loc[:, 'date']


# Target
#target_name = 'Dumbell incline press 30 degrees'
#target_name = 'Squats'
#target_name = 'Lat pulldowns'
target_name = 'Benchpress'
target = dfo[target_name]
interpolated_target = dfo['orm_interpolated'] = target.replace(0, method='pad')

# Features
# Workout day feature
dfo['workout_day'] = (dfo['weightVolume'] > 0).astype(int)
# create a rolling average of the ORM over time
#rolling_avg = interpolated_target.rolling(window=14, min_periods=4, center=False).mean()
#rolling_avg.fillna(0, inplace=True)

y = pd.DataFrame(interpolated_target, index=dfo.index)
X = make_lags(y, 7).fillna(0)
y = make_multistep_target(y, steps=14).dropna()

# Shifting has created indexes that don't match. Only keep times for
# which we have both targets and features.
y, X = y.align(X, join='inner', axis=0)
print(y)
print(X)

# Create splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

model = KNeighborsRegressor()
model.fit(X_train, y_train)
y_fit = pd.DataFrame(model.predict(X_train), index=X_train.index, columns=y.columns)
y_pred = pd.DataFrame(model.predict(X_test), index=X_test.index, columns=y.columns)

# create a pd.Series with dates for y_pred
forecasted_dates = pd.date_range(start=dates.max(), periods=14, freq='D')
print(X_test)
print(y_test)
# plot a single plot
fig, ax = plt.subplots()
ax.scatter(target.index, target, color='grey', label=f'{target_name} ORM')
ax.plot(y_pred.index, y_pred, color='blue', label='Trend')
#ax.plot(rolling_avg.index, rolling_avg, color='black', label='Rolling average')
ax.plot(y_fit.index, y_fit, label='y_fit')
ax.set_title(f'{target_name} ORM')
ax.set_xlabel('Date')
ax.set_ylabel('ORM')
ax.legend()
plt.show()