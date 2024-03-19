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
dataset_volume = ld.load(path='volume.csv')
targetname = 'Benchpress'

# interpolate one-rep-max for the target
dataset['orm_interpolated'] = dataset[targetname].replace(0, method='pad')
dataset_volume['volume_interpolated'] = dataset_volume[targetname].replace(0, method='pad')
# drop all rows with 0 values for the target
dataset = dataset[dataset['orm_interpolated'] > 0]

print(dataset
      )
dataset.index = pd.to_datetime(dataset.index)
dataset['days_since_last_workout'] = (dataset.index.to_series().diff().dt.days).fillna(0).cumsum()

features = pd.concat([dataset[['orm_interpolated', 'days_since_last_workout']], dataset_volume['volume_interpolated']], axis=1)

# Make index start at 0 
features = features[features['orm_interpolated'] > 0]
features.index = range(len(features))

# Normalize the features
scaler = MinMaxScaler(feature_range=(0, 1))
features_scaled = scaler.fit_transform(features)

def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i+n_steps])
        y.append(data[i+n_steps, 0])  # Assuming the first column is the target (orm_interpolated)
    return np.array(X), np.array(y)

# Define the number of time steps to consider
n_steps = 90
n_features = features_scaled.shape[1]  # Number of features

# Create sequences of data
X, y = create_sequences(features_scaled, n_steps)
# Reshape the input data for LSTM (samples, time steps, features)
X = X.reshape((X.shape[0], n_steps, n_features))

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(n_steps, n_features)))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=5, batch_size=1)

# Prediction setup (adapted for the multi-feature scenario)
future_steps = 60
X_test = features_scaled[-n_steps:].reshape(1, n_steps, n_features)
predictions = []

for _ in range(future_steps):
    prediction = model.predict(X_test)
    predictions.append(prediction[0, 0])
    prediction_expanded = np.expand_dims(prediction, axis=0)
    X_test = np.append(X_test[:, 1:, :], prediction_expanded[:, :, :1], axis=1)  # Adapt for multiple features

# Inverse transform the predictions to the original scale
predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# Adjust plotting code to remove trend and update labels
plt.plot(range(len(y)), scaler.inverse_transform(X[:, :, 0])[:, 0], label='Actual ORM')
plt.plot(np.arange(len(y), len(y) + future_steps), predictions, label='Predicted ORM')
plt.xlabel('Time Steps')
plt.ylabel('One-Rep-Max')
plt.title(f'One-Rep-Max Forecast {targetname}')
plt.legend()
plt.show()