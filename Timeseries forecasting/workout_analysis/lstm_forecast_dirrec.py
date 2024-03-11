from tensorflow.keras.models import load_model
import os
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import load_data as ld

dataset_path = 'onerepmax.csv'
model_path = 'models/model.h5'
n_steps = 150 # Number of time steps to consider

dataset = ld.load(path=dataset_path)
dataset['orm_interpolated'] = dataset[targetname].replace(0, method='pad')
target = pd.DataFrame(dataset['orm_interpolated'], index=dataset.index)
target = target[target['orm_interpolated'] > 0]

# Function to check if the model exists and load it
def load_model_from_file(model_path):
    if os.path.exists(model_path):
        print("Loading the trained model...")
        model = load_model(model_path)
    return model

def predict_future_strength(targetname, future_steps):
    scaler = MinMaxScaler(feature_range=(0, 1))
    target_scaled = scaler.fit_transform(target)

    X_test = target_scaled[-n_steps:].reshape(1, n_steps, 1)
    predictions = []

    for i in range(future_steps):
        prediction = model.predict(X_test)
        predictions.append(prediction[0, 0])
        prediction_expanded = np.expand_dims(prediction, axis=1)
        X_test = np.append(X_test[:, 1:, :], prediction_expanded, axis=1)
        pred_rescaled = scaler.inverse_transform(prediction)
        print(str(pred_rescaled[0][0]))
    return predictions

model = load_model_from_file(model_path)
def load_model():
    global model
    model = load_model_from_file(model_path)

predictions = predict_future_strength('Benchpress', 60)

# plot predictions and actual values
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(150, 150+len(predictions)), predictions, label='Predicted')
plt.plot(target.index[-60:], target['orm_interpolated'].values[-60:], label='Actual')
plt.xlabel('Time Steps')
plt.ylabel('One-Rep Max')
plt.show()