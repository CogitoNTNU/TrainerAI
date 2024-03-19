
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
import pandas as pd
import matplotlib.pyplot as plt
from load_data import load

dfo = load(path='data/onerepmax.csv')

plot_acf(dfo['Benchpress'], lags=120)  # Adjust lags as needed
plt.show()