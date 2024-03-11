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
n_steps = 180

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
model.fit(X, y, epochs=10, batch_size=1)

# Use the trained model to predict future values
future_steps = 60
X_test = target_scaled[-n_steps:].reshape(1, n_steps, 1)

predictions_existing_data = model.predict(X)

# Reshape the predictions to match the original scale
predictions_existing_data = predictions_existing_data.reshape(-1, 1)
predictions_existing_data = scaler.inverse_transform(predictions_existing_data)

print(target)

# Plot the results for the existing data
plt.figure(figsize=(10, 6))
plt.plot(target.index[n_steps:], target['orm_interpolated'].values[n_steps:], label='Actual')
plt.plot(target.index[n_steps:], predictions_existing_data, label='Predicted (Existing Data)')
plt.xlabel('Time Steps')
plt.ylabel('One-Rep-Max')
plt.legend()
plt.title('Prediction along Existing Data')
plt.show()