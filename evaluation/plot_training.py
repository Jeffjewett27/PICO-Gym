import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('logs/celeste_t4.old.monitor.csv', header=1)
df = pd.read_csv('logs/celeste_t4b.monitor.csv', header=1)
# df['l'] = df['l'].rolling(30000).mean()
# df['r'] = df['r'].rolling(3000).mean()
# resolution = 10000
# s = (df.index.to_series() / resolution).astype(int)

# df.groupby(s).std().set_index(s.index[resolution-1::resolution])
df['time'] = pd.to_datetime(df['t'], unit='s')
df = df.set_index('time')
print(df)
# df = df.resample('5S').quantile(0.25)
# df = df.resample('50S').mean()
df = df.resample('50S').apply(lambda x: x[x['tag'] == 'goal']['tag'].count()/ len(x))
print(df.head())

df.plot(x='t')

plt.show()