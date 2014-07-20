# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import cm
from scipy.stats import norm
import numpy as np
import datetime as dt
import pandas as pd

def load_data_as_series(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  return pd.Series(data[:,1], time)

def load_data_as_dataframe(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  #data[:,0] = pd.to_datetime(data[:,0])
  #time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  retval = pd.DataFrame(data, columns = ['ts', 'freq'])
  retval['ts'] = retval['ts'].astype(int)
  retval['freq'] = retval['freq'].astype(float)
  retval['ts'] = pd.to_datetime(retval['ts'], unit='s')
  retval['date'] = [c.date() for c in retval['ts']]
  retval['time'] = [c.time() for c in retval['ts']]
  return retval

df = load_data_as_dataframe("datasets/20140718-export.txt")
minfreq = np.min(df['freq'])
maxfreq = np.max(df['freq'])
df['color'] = [(f - minfreq)/maxfreq for f in df['freq']]
df['color'] = df['color'].astype(int)
print df.head()
plt.scatter(df['date'], df['time'], c=1)

#ts = load_data_as_series("datasets/20140718-export.txt")
#plt.close('all')
#
## see http://pandas.pydata.org/pandas-docs/stable/visualization.html
#plt.title("Verlauf der Netzfrequenz")
#plt.xlabel("Zeit")
#plt.ylabel("Frequenz [Hz]")
#ts.plot(colormap=cm.cubehelix, label="Defluxio")
#
#plt.figure(2)
#min_ts = ts.resample('1Min')
#plt.title("Netzfrequenz: Minuten-Werte")
#plt.xlabel("Zeit")
#plt.ylabel("Frequenz [Hz]")
#min_ts.plot(colormap=cm.cubehelix, label="Defluxio")
#
#
## plt.figure(3)
## https://stackoverflow.com/questions/24398497/pandas-how-to-stack-time-series-into-a-dataframe-with-time-columns?rq=1
#
##plt.legend()


plt.show()
