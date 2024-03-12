# Getting started

## Create a virtual environment using:
```
python -m venv venv
```

## Activate it:
### Windows
```
.\venv\Scripts\activate
```
### Mac
```
source venv/bin/activate
```

## Install dependencies
```
pip install tensorflow scikit-learn numpy pandas matplotlib statsmodels xgboost seaborn
```

# Scripts overview

## Timeseries forecasting

### autocorrelation.py
Let's you see the autocorrelation for a uni-variate timeseries.
In plain english, that means it's a graph showing how much the previous values affect the current value.

### boosted_hybrid.py
A 2 layer model using linear correlation and XGBoost to fit on multiple features.

### lstm_compared_to_data.py
Runs an lstm model on the training data, showing how the lstm model fits compared to the interpolated data.
This script can't predict, as it lacks the ability to create future datapoints.

### lstm_forecast_dirrec.py
An lstm model trained on a uni-variate timeseries.
This predicts the future values, by predicting one value, then appending it to the existing timeseries.
Then it predicts the next value using all previous available data, including the value it predicted by itself.
This method is prone to weird results if you try to predict long-term.
It also only uses 1 feature, so it can be greatly improved.