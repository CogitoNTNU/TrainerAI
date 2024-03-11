
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf

import pandas as pd
import matplotlib.pyplot as plt
from load_data import load

dfo = load(path='onerepmax.csv')

plot_acf(dfo['Lat pulldowns'], lags=40)  # Adjust lags as needed
plt.show()



#result = seasonal_decompose(df['Benchpress'], model='additive', period=7)
#result.plot()
#plt.show()

# Plot autocorrelation of the target to determine lags
#plot_acf(target, lags=30)
#plt.show()