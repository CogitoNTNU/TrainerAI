from tensorflow.keras.models import load_model
import os
from flask import Flask, jsonify
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import load_data as ld

# Function to check if the model exists and load it
def load_custom_model(model_path):
    if os.path.exists(model_path):
        print("Loading the trained model...")
        model = load_model(model_path)
    return model

def predict_future_strength(targetname, future_steps):
    n_steps = 150
    dataset = ld.load(path='onerepmax.csv')
    dataset['orm_interpolated'] = dataset[targetname].replace(0, method='pad')
    target = pd.DataFrame(dataset['orm_interpolated'], index=dataset.index)
    target = target[target['orm_interpolated'] > 0]
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
        emit('prediction_response', {'prediction': str(pred_rescaled[0][0]), 'index': i})
    return predictions

app = Flask(__name__)

model_path = 'path/to/your_model.h5'  # Define the model save/load path
model = load_custom_model(model_path)
def updateModel():
    global model
    model = load_custom_model(model_path)

print("loading model...")
updateModel()
print("Model loaded")

app = Flask(__name__)

@app.route('/')
def index():
    return "Timeseries!!"

@app.route('/predict')
def predict(data):
    print(data)
    target = data['target'] # The exercise to target
    days = data['days'] # Steps into the future
    predict_future_strength(target, days)

if __name__ == '__main__':
    app.run(debug=True, port=3002, host='0.0.0.0')