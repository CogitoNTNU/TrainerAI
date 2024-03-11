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
interpolated_target = dfv['orm_interpolated'] = target.replace(0, method='pad')
# create a rolling average of the ORM over time
rolling_avg = interpolated_target.rolling(window=14, min_periods=4, center=False).mean()
rolling_avg.fillna(0, inplace=True)

# Plot autocorrelation of the target to determine lags
#plot_acf(target, lags=30)
#plt.show()

# Workout day feature
dfv['workout_day'] = (dfv['weightVolume'] > 0).astype(int)

model = bh.BoostedHybrid(LinearRegression(), XGBRegressor())

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
X_2 = dfv.loc[:, ['workout_day', 'weightVolume', 'orm_interpolated']]

model.fit(X_1, X_2, y)

last_date = dfo['date'][len(dfo['date'])-1] # Get the last date in your existing data
future_dates = pd.date_range(start=last_date, periods=15, freq='D')[1:]  # 15 to include the last date
full_dates = pd.concat([dfo['date'], pd.Series(future_dates)]) # wabt to add the future dates to the plot

# Create future_X_1 using DeterministicProcess for future dates
future_dp = DeterministicProcess(
    index=future_dates,
    constant=False,
    order=2,
    drop=True,
)
days = 14
last_orm = dfv['orm_interpolated'][len(dfv['orm_interpolated'])-1]
future_X_1 = future_dp.out_of_sample(steps=days)
# Take the last value of X_1 and start future_X_1 index from there
print(future_dates)
future_X_1.index = future_dates

future_X_2 = pd.DataFrame({
    'workout_day': [1] * days,  # Assuming no workout on future dates
    'weightVolume': [3500] * days,  # Placeholder for weightVolume
    'orm_interpolated': [last_orm] * days,  # Placeholder for orm_interpolated
}, index=future_dates)

y_pred = model.predict(X_1, X_2)
print(future_X_1)
print(X_1)
y_future = model.predict(future_X_1, future_X_2, steps=14)
print(y_future)

print("Length of full_dates:", len(full_dates))
print("Length of target:", len(target))

# plot a single plot
fig, ax = plt.subplots()
ax.scatter(full_dates[:len(target)], target, color='grey', label=f'{target_name} ORM')
ax.plot(dfo['date'], y_pred, color='blue', label='Trend')
ax.plot(dfo['date'], rolling_avg, color='black', label='Rolling average')
#ax.plot(dfo['date'], model.y_fit, label='y_fit')
#ax.plot(dfo['date'], model.y_resid, label='y_resid')
ax.set_title(f'{target_name} ORM')
ax.set_xlabel('Date')
ax.set_ylabel('ORM')
ax.legend()
plt.show()