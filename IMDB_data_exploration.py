import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

df_train = pd.read_csv('movies.csv')
print(df_train)
print(df_train.columns)
print(df_train['us_grossMillions'].describe())
sns.distplot(df_train['us_grossMillions'])
plt.show()
print("Skewness: %f" % df_train['us_grossMillions'].skew())
print("Kurtosis: %f" % df_train['us_grossMillions'].kurt())

data1 = pd.concat([df_train['us_grossMillions'], df_train['timeMin']], axis=1)
data1.plot.scatter(x='timeMin', y='us_grossMillions')
plt.show()

data2 = pd.concat([df_train['us_grossMillions'], df_train['imdb']], axis=1)
data2.plot.scatter(x='imdb', y='us_grossMillions')
plt.show()

data3 = pd.concat([df_train['us_grossMillions'], df_train['metascore']], axis=1)
data3.plot.scatter(x='metascore', y='us_grossMillions')
plt.show()

data4 = pd.concat([df_train['us_grossMillions'], df_train['votes']], axis=1)
data4.plot.scatter(x='votes', y='us_grossMillions')
plt.show()

data5 = pd.concat([df_train['us_grossMillions'], df_train['year']], axis=1)
fig = sns.boxplot(x='year', y='us_grossMillions', data=data5)
# plt.xticks(rotation=90)
plt.show()


