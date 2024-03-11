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

target = pd.DataFrame(dataset['orm_interpolated'], index=dataset.index)
target = target[target['orm_interpolated'] > 0]
# Make index start at 0 
target.index = range(len(target))

# remove all target values that are 0 from beginning of the dataset
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
n_steps = 150
# Create sequences of data
X, y = create_sequences(target_scaled, n_steps)
# Reshape the input data for LSTM (samples, time steps, features)
X = X.reshape(X.shape[0], X.shape[1], 1)

model_path = 'models/model.h5'

model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(X.shape[1], 1), return_sequences=True))
model.add(LSTM(units=25, activation='relu', return_sequences=False))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X, y, epochs=32, batch_size=8, verbose=1)
model.save(model_path)

fut_steps = 60
def predict_future_strength(future_steps):
    X_test = target_scaled[-n_steps:].reshape(1, n_steps, 1)
    predictions = []
    fut_steps = future_steps

    for i in range(future_steps):
        prediction = model.predict(X_test)
        predictions.append(prediction[0, 0])
        prediction_expanded = np.expand_dims(prediction, axis=1)
        X_test = np.append(X_test[:, 1:, :], prediction_expanded, axis=1)
    return predictions

predictions = predict_future_strength(60)
    
# Inverse transform the predictions to the original scale
predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

print(target.index)
print(target['orm_interpolated'])
# Plot the results
plt.plot(target.index, target['orm_interpolated'], label='Actual')
plt.plot(target.index, y_pred, label='Trend')
plt.plot(np.arange(len(target), len(target)+fut_steps), predictions, label='Predicted')
plt.xlabel('Time Steps')
plt.ylabel('One-Rep-Max')
plt.title(f'One-Rep-Max Forecast {targetname}')
plt.legend()
plt.show()