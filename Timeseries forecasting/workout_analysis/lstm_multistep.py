import numpy as np
import pandas as pd
import tensorflow as tf
import load_data as ld
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

dataset = ld.load(path='onerepmax.csv')
target = 'Benchpress'

dataset['workout_day'] = (dataset['weightVolume'] > 0).astype(int)
dataset['orm_interpolated'] = dataset[target].replace(0, method='pad')

target = pd.DataFrame(dataset['orm_interpolated'], index=dataset.index)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
target_scaled = scaler.fit_transform(target)

def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data)-n_steps):
        X.append(data[i:i+n_steps, 0])
        y.append(data[i+n_steps, 0])
    return np.array(X), np.array(y)

# Define the number of time steps to consider
n_steps = 365

# Create sequences of data
X, y = create_sequences(target_scaled, n_steps)
# Reshape the input data for LSTM (samples, time steps, features)
X = X.reshape(X.shape[0], X.shape[1], 1)

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(n_steps, 1)))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=100, batch_size=1)

# Use the trained model to predict future values
future_steps = 180
X_test = target_scaled[-n_steps:].reshape(1, n_steps, 1)

# Predict the entire sequence of future_steps
predictions = model.predict(X_test)
for _ in range(future_steps - 1):
    # Update X_test with the true future value (if available)
    # You need to have the actual future values for this
    # For demonstration purposes, you can replace this with your actual future data
    true_future_value = target_scaled[len(X_test[0])]
    X_test = np.append(X_test[:, 1:, :], np.expand_dims(np.expand_dims(true_future_value, axis=0), axis=2), axis=1)

    # Predict the next timestep using the updated X_test
    next_prediction = model.predict(X_test)
    predictions = np.append(predictions, next_prediction)

# Reshape the predictions to match the original scale
predictions = predictions.reshape(-1, 1)
predictions = scaler.inverse_transform(predictions)

# Plot the results
plt.plot(target.index, target['orm_interpolated'], label='Actual')
plt.plot(np.arange(len(target), len(target)+future_steps), predictions, label='Predicted')
plt.xlabel('Time Steps')
plt.ylabel('One-Rep-Max')
plt.legend()
plt.show()