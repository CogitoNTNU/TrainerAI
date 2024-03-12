import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from load_data import load
from statsmodels.tsa.deterministic import DeterministicProcess
from statsmodels.graphics.tsaplots import plot_acf
import numpy as np
from scipy.stats import pearsonr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

dfv = load(path='data/volume.csv')
dfo = load(path='data/onerepmax.csv')
dates = dfo.loc[:, 'date']

# Assuming dfv and dfo are DataFrames loaded from 'data.csv' and 'onerepmax.csv' respectively

orm = 'Benchpress'
volume = 'Benchpress'
volume2 = 'Lat pulldowns'
# Replace 0 values in the specified columns with the previous non-zero value
secondary_volume = dfv[volume2].replace(0, method='pad')
target_volume = dfv[volume].replace(0, method='pad')
target_orm = dfo[orm].replace(0, method='pad')
# remove 0 values from the target_orm, secondary_volume, and target_volume
target_orm = target_orm[target_orm > 0]
secondary_volume = secondary_volume[secondary_volume > 0]
target_volume = target_volume[target_volume > 0]
# remove nan
target_orm = target_orm.dropna()
secondary_volume = secondary_volume.dropna()
target_volume = target_volume.dropna()
# Remove all rows that secondary_volume and target_volume do not have in common
target_orm = target_orm[target_orm.index.isin(secondary_volume.index)]
target_volume = target_volume[target_volume.index.isin(secondary_volume.index)]
secondary_volume = secondary_volume[secondary_volume.index.isin(target_volume.index)]

print(target_orm)
print(secondary_volume)
print(target_volume)

# Create a new DataFrame with the relevant columns
data = pd.DataFrame({
    f'{volume2} Volume': secondary_volume,
    f'{volume} Volume': target_volume,
    f'{orm} ORM': target_orm
})

# Calculate the correlation matrix
correlation_matrix = data.corr()

# Extract the correlation coefficient between Bench Press ORM and Squats Volume
correlation_coefficient, _ = pearsonr(data[f'{orm} ORM'], data[f'{volume2} Volume'])

# Plotting the heatmap for the correlation matrix
plt.figure(figsize=(12, 5))

# Subplot for the correlation matrix heatmap
plt.subplot(1, 2, 1)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix')

# Subplot for the scatter plot of Bench Press ORM and Squats Volume
plt.subplot(1, 2, 2)
sns.scatterplot(x=f'{orm} ORM', y=f'{volume2} Volume', data=data)
plt.title(f'Scatter Plot (Correlation: {correlation_coefficient:.2f})')
plt.xlabel(f'{orm} ORM')
plt.ylabel(f'{volume2} Volume')

# Linear graphs
plt.figure(figsize=(12, 5))

# Subplot for the linear graph of Bench Press Volume
plt.subplot(1, 2, 1)
sns.regplot(x=f'{volume} Volume', y=f'{orm} ORM', data=data, line_kws={'color': 'red'})
plt.title('Linear Graph: Bench Press Volume vs. Bench Press ORM')

# Subplot for the linear graph of Squats Volume
plt.subplot(1, 2, 2)
sns.regplot(x=f'{volume2} Volume', y=f'{orm} ORM', data=data, line_kws={'color': 'green'})
plt.title(f'Linear Graph: {volume2} Volume vs. {orm} ORM')

# Adjust layout for better spacing
plt.tight_layout()

plt.show()