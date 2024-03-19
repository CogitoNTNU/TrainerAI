import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import load_data as ld
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.deterministic import DeterministicProcess

dataset = ld.load(path='onerepmax.csv')
targetname = 'Benchpress'

# Create a feature for workout days
dataset['workout_day'] = (dataset['weightVolume'] > 0).astype(int)
# interpolate one-rep-max for the target
dataset['orm_interpolated'] = dataset[targetname].replace(0, method='pad')
# drop all rows with 0 values for the target
dataset = dataset[dataset['orm_interpolated'] > 0]

# Create a linear regression model
dp = DeterministicProcess(
    index=dataset.index,  # dates from the training data
    constant=False,       # dummy feature for the bias (y_intercept)
    order=1,           # the time dummy (trend) polynomial order.
    drop=True,           # drop terms if necessary to avoid collinearity
)
# Create a linear regression model
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=60)
model = LinearRegression()
y = dataset['orm_interpolated']
model.fit(X, y)
y_pred = pd.Series(model.predict(X), index=X.index)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)
# Create a linear trend feature
dataset['linear_trend'] = y_pred

features = dataset[['workout_day', 'weightVolume', 'orm_interpolated', 'linear_trend']]
target = dataset[['orm_interpolated']]
# Make index start at 0
target.index = range(len(target))
features.index = range(len(features))

# Normalize the data
targetscaler = MinMaxScaler(feature_range=(0, 1))
target_scaled = targetscaler.fit_transform(target)

scaler = MinMaxScaler(feature_range=(0, 1))
features_scaled = scaler.fit_transform(features)

def create_sequences_multivariate(target_data, features_data, n_steps):
    X, y = [], []
    for i in range(len(target_data)-n_steps):
        X.append(features_data[i:i+n_steps, :]) # All features as input
        y.append(target_data[i+n_steps, 0])
    return np.array(X), np.array(y)

n_steps = 90

# Create sequences of data
X, y = create_sequences_multivariate(target_scaled, features_scaled, n_steps)

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(n_steps, features.shape[1]), return_sequences=True))
model.add(LSTM(units=25, activation='relu', input_shape=(n_steps, features.shape[1]), return_sequences=False))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=1, batch_size=1)

# Use the trained model to predict future values
future_steps = 14
X_test = features_scaled[-n_steps:].reshape(1, n_steps, features.shape[1])
predictions = []

# Get the average weightVolume historically
historical_weightVolume_avg = features['weightVolume'].mean()

rest_days = features['workout_day'].mean()
rest_days = round(1 / rest_days)+3
last_workout_day_index = len(target) % rest_days
print(rest_days)

for i in range(future_steps):
    prediction = model.predict(X_test)
    predictions.append(prediction[0, 0])
    prediction_expanded = np.zeros((1, features.shape[1]))  # Create a zero array with the shape of (1, number of features)
    prediction_expanded[0, features.columns.get_loc("orm_interpolated")] = prediction[0, 0]
    # Increment the linear trend or keep it constant; adjust based on your model's linear trend calculation
    prediction_expanded[0, features.columns.get_loc("linear_trend")] = features['linear_trend'].iloc[-1]  # Keeping the last trend value
    prediction_expanded[0, features.columns.get_loc("workout_day")] = 1 if (i + last_workout_day_index) % rest_days == 0 else 0
    prediction_expanded[0, features.columns.get_loc("weightVolume")] = historical_weightVolume_avg if (i + last_workout_day_index) % rest_days == 0 else 0
    prediction_expanded = prediction_expanded.reshape(1, 1, features.shape[1])
    X_test = np.append(X_test[:, 1:, :], prediction_expanded, axis=1)
    
print(predictions)
# Inverse transform the predictions to the original scale
predictions = targetscaler.inverse_transform(np.array(predictions).reshape(-1, 1))
print(predictions)

for i in range(future_steps):
    features.at[len(target) + i, 'workout_day'] = 1 if (i + last_workout_day_index) % rest_days == 0 else 0
    features.at[len(target) + i, 'weightVolume'] = historical_weightVolume_avg if (i + last_workout_day_index) % rest_days == 0 else 0
    # Assuming you keep the last trend value constant or adjust as needed
    features.at[len(target) + i, 'linear_trend'] = features['linear_trend'].iloc[-1]

# Plot all features in a single plot
fig, ax = plt.subplots(4, 1, figsize=(10, 10))
print(target_scaled)
print(features_scaled)
print(target.index)
print(predictions)
ax[0].plot(target.index, target['orm_interpolated'], label='Actual')
ax[0].plot(np.arange(len(target), len(target)+future_steps), predictions, label='Predicted')
ax[0].set_xlabel('Time Steps')
ax[0].set_ylabel('One-Rep-Max')
ax[0].set_title(f'One-Rep-Max Forecast {targetname}')
ax[0].legend()
ax[1].plot(features.index, features['workout_day'], label='Workout Day')
ax[1].set_xlabel('Time Steps')
ax[1].set_ylabel('Workout Day')
ax[1].legend()
ax[2].plot(features.index, features['weightVolume'], label='Weight Volume')
ax[2].set_xlabel('Time Steps')
ax[2].set_ylabel('Weight Volume')
ax[2].legend()
ax[3].plot(features.index, features['linear_trend'], label='Linear Trend')
ax[3].set_xlabel('Time Steps')
ax[3].set_ylabel('Linear Trend')
ax[3].legend()
plt.show()