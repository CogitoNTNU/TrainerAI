import json
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.linear_model import LinearRegression

# load csv file 'data.csv' into pandas dataframe
df = pd.read_csv('data.csv', parse_dates=['date'])
#print(df.describe())

# Remove hours, minutes, and seconds from the date column
df['date'] = df['date'].dt.date
df['date'] = pd.to_datetime(df['date'])

dates = df.loc[:, 'date']
print(df.head())
# create new dataframe with a row for all dates in the range
new_df = pd.DataFrame({'date': pd.date_range(start=dates.min(), end=dates.max(), freq='D')})
print(new_df.head())
# merge the new dataframe with the original dataframe, so that all dates are included
df = pd.merge(new_df, df, on='date', how='left')
df.fillna(0, inplace=True)

print(df.index)
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
print(X_fore)
y = df['weightVolume']

model.fit(X, y)
y_pred = pd.Series(model.predict(X), index=X.index)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

# create a new pd.Series with dates for the next 30 days
forecasted_dates = pd.date_range(start=dates.max(), periods=30, freq='D')

# plotting
fig, ax = plt.subplots()

# Plot the bar chart on the first axis
# Create a second axis to overlay the line plot
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