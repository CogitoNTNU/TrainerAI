import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from load_data import load
from statsmodels.tsa.deterministic import DeterministicProcess
import numpy as np
import simpleBoost as bh
from xgboost import XGBRegressor

# Load data
dfv = load(path='data.csv')
dates = dfv.loc[:, 'date']
dfo = load(path='onerepmax.csv')

# Target
#target_name = 'Dumbell incline press 30 degrees'
#target_name = 'Squats'
#target_name = 'Lat pulldowns'
target_name = 'Benchpress'
target = dfo[target_name]
interpolated_target = dfo['orm_interpolated'] = target.replace(0, method='pad')
# create a rolling average of the ORM over time
rolling_avg = interpolated_target.rolling(window=14, min_periods=4, center=False).mean()
rolling_avg.fillna(0, inplace=True)

# Plot autocorrelation of the target to determine lags
#plot_acf(target, lags=30)
#plt.show()

# Workout day feature
dfv['workout_day'] = (dfv['weightVolume'] > 0).astype(int)

model = bh.BoostedHybrid(LinearRegression(), XGBRegressor())

# Target series
y = pd.Series(interpolated_target, index=dfo.index)
# X_1 features for linear regression
dp = DeterministicProcess(
    index=dfo.index,  # dates from the training data
    constant=False,       # dummy feature for the bias (y_intercept)
    order=2,           # the time dummy (trend) polynomial order.
    drop=True,           # drop terms if necessary to avoid collinearity
)
X_1 = dp.in_sample()

# X_2 features for xgboost
X_2 = dfv.loc[:, ['weightVolume', 'workout_day', 'Benchpress']] # benchpress volume
print(X_2)

model.fit(X_1, X_2, y)
y_pred = model.predict(X_1, X_2)

# plot a single plot
fig, ax = plt.subplots()
ax.scatter(dfo['date'], target, color='grey', label=f'{target_name} ORM')
ax.plot(dfo['date'], y_pred, color='blue', label='Trend')
#ax.plot(dfo['date'], rolling_avg, color='black', label='Rolling average')
ax.plot(dfo['date'], model.y_fit, label='y_fit')
#ax.plot(dfo['date'], model.y_resid, label='y_resid')
ax.set_title(f'{target_name} ORM')
ax.set_xlabel('Date')
ax.set_ylabel('ORM')
ax.legend()
plt.show()