import json
import pathlib
from statsmodels.tsa.deterministic import DeterministicProcess
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from load_data import load

df = load(path='data.csv')
dates = df.loc[:, 'date']

dp = DeterministicProcess(
    index=df.index,  # dates from the training data
    constant=False,       # dummy feature for the bias (y_intercept)
    order=2,           # the time dummy (trend) polynomial order.
    drop=True,           # drop terms if necessary to avoid collinearity
)

# create a rolling average of the volume over time
# rolling_avg = df['weightVolume'].rolling(window=7, min_periods=4, center=True).mean()
# rolling_avg.fillna(0, inplace=True)
# print(rolling_avg)
# Add the rolling average to the DataFrame
# df['rolling'] = rolling_avg

model = LinearRegression()
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=30)
y = df['weightVolume']

model.fit(X, y)
y_pred = pd.Series(model.predict(X), index=X.index)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

# create a new pd.Series with dates for the next 30 days
forecasted_dates = pd.date_range(start=dates.max(), periods=30, freq='D')

fig, ax = plt.subplots()
#ax2 = ax.twinx()
ax.bar(df['date'], df['weightVolume'], color='black', label='Volume')
ax.plot(df['date'], y_pred, color='blue', label='Trend')
ax.plot(forecasted_dates, y_fore, color='red', label='Future Trend')
# Set labels and title for the first axis
ax.set_xlabel('Date')
ax.set_ylabel('Volume', color='blue')
ax.set_title('Volume and trend Over Time')
# Set labels and title for the second axis
#ax2.set_ylabel('Trend', color='red')
ax.legend(loc='upper left')
#ax2.legend(loc='upper right')
# Display the plot
plt.show()

""" 
Schema for workouts:
    _id
    dateTime
    exercisesJson
    Array (3)
    ownerId (NOT owner_id or owner_Id)
    personalNote
    reps
    sets
    weightVolume
    duration
"""