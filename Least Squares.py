import pandas as pd
import numpy as np

# Data Matrix
df_train = pd.read_csv('movies.csv')
df_train['metascore'].fillna(78.280095, inplace=True)
df_train['us_grossMillions'].fillna(67.637564, inplace=True)
Data = df_train.values
Data = np.delete(Data, 0, 1)
Data = np.delete(Data, 4, 1)
Data = np.delete(Data, 0, 1)
Data = np.delete(Data, 3, 1)

# Y
Y = df_train['us_grossMillions'].values

# Parameter Vector
YTD = np.matmul(Y, Data)
DataT = Data.transpose()
DTD = np.matmul(DataT, Data)
DTD = DTD.astype("float64")
DTDI = np.linalg.pinv(DTD)
theta = np.matmul(YTD, DTDI)

# Estimation
xn = np.array([7.6, 68.0, 335000])
yn = np.matmul(theta.transpose(), xn)
print(yn)
