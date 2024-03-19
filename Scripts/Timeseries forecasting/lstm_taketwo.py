import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import load_data as ld
import seaborn as sns
import matplotlib.pyplot as plt

targetname = 'Benchpress'
# Load the data
dataset = ld.load(path='onerepmax.csv')
# Create a feature for workout days
dataset['workout_day'] = (dataset['weightVolume'] > 0).astype(int)
# interpolate one-rep-max for the target
dataset['orm_interpolated'] = dataset[targetname].replace(0, method='pad')
print(dataset['orm_interpolated'])
# drop all rows with 0 values for the target
dataset = dataset[dataset['orm_interpolated'] > 0]




# Assuming 'dataset' is your DataFrame and already loaded
# Generate 'workout_day' and ensure 'orm_interpolated' is correctly set up
dataset['workout_day'] = (dataset['weightVolume'] > 0).astype(int)

# Select features and target
features = dataset[['orm_interpolated', 'workout_day']]
target = dataset['orm_interpolated']

# Normalize the features
scaler = MinMaxScaler(feature_range=(0, 1))
features_scaled = scaler.fit_transform(features)

target_scaler = MinMaxScaler(feature_range=(0, 1))
target_scaled = target_scaler.fit_transform(target.values.reshape(-1, 1))

# Define a function to create sequences
def create_sequences(features, target, n_steps):
    X, y = [], []
    for i in range(len(features) - n_steps):
        X.append(features[i:i+n_steps])
        y.append(target[i+n_steps])
    return np.array(X), np.array(y)

n_steps = 120  # Number of time steps to look back
X, y = create_sequences(features_scaled, target_scaled, n_steps)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_steps, X.shape[2]), return_sequences=True))
model.add(LSTM(50, activation='relu', input_shape=(n_steps, X.shape[2]), return_sequences=False))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model.fit(X_train, y_train, epochs=200, verbose=1, batch_size=32, validation_split=0.2)

# Evaluate the model
mse = model.evaluate(X_test, y_test, verbose=0)
print(f'Test MSE: {mse}')

# Make predictions
predictions = model.predict(X_test)

# Invert the predictions
predictions = target_scaler.inverse_transform(predictions)
y_test = target_scaler.inverse_transform(y_test)


# Assuming you have 'predictions' and 'y_test' already inverse transformed
# Create a DataFrame for the predictions with a corresponding index
predictions_df = pd.DataFrame(predictions, columns=['Predicted ORM'])
predictions_df.index = np.arange(len(dataset) - len(predictions), len(dataset))

# Create a DataFrame for the actual ORM with a corresponding index
actual_orm_df = pd.DataFrame(dataset['orm_interpolated'].values, columns=['Actual ORM'])
actual_orm_df.index = np.arange(len(dataset))

# Combine the historical and predicted ORM into one DataFrame
combined_orm_df = pd.concat([actual_orm_df, predictions_df], axis=1)

# Plot using Seaborn
plt.figure(figsize=(14, 7))
sns.lineplot(data=combined_orm_df['Actual ORM'], label='Historical ORM', color='blue')
sns.lineplot(data=combined_orm_df['Predicted ORM'], label='Predicted ORM', color='orange')

plt.title('Historical and Predicted One-Rep Max')
plt.xlabel('Time')
plt.ylabel('One-Rep Max (ORM)')
plt.legend()
plt.show()