import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

class BoostedHybrid:
    def __init__(self, model_1, model_2):
        self.model_1 = model_1
        self.model_2 = model_2
        self.y_columns = None  # store column names from fit method

def fit(self, X_1, X_2, y):
    # YOUR CODE HERE: fit self.model_1
    self.model_1.fit(X_1, y)

    y_fit = pd.DataFrame(
        self.model_1.predict(X_1),
        index=X_1.index, 
    )

    # YOUR CODE HERE: compute residuals
    y_resid = (y - y_fit.squeeze())
    y_resid = y_resid.squeeze() # wide to long
    self.model_2.fit(X_2, y_resid)

    self.y_fit = y_fit
    self.y_resid = y_resid

def predict(self, X_1, X_2, future_X_1=None, future_X_2=None, steps=0):
    # Predict using self.model_1
    y_pred = self.model_1.predict(X_1)

    # If future_X_1 and future_X_2 are provided, predict future steps
    if future_X_1 is not None and future_X_2 is not None and steps > 0:
        # Initialize an array to store future predictions
        future_preds = []

        # Loop for each step into the future
        for step in range(steps):
            # Make predictions for the future step using both models
            future_pred_step = self.model_1.predict(future_X_1.iloc[[step]]) + self.model_2.predict(future_X_2.iloc[[step]])
            future_preds.append(future_pred_step.item())
        # Append future predictions to y_pred
        y_pred = np.concatenate((y_pred, future_preds))
    else:
        # If no future_X_1 and future_X_2 provided, use only self.model_1
        
        y_pred += self.model_2.predict(X_2)

    return y_pred

# Add method to class
BoostedHybrid.predict = predict

# Add method to class
BoostedHybrid.fit = fit