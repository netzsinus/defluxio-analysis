# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl
import matplotlib.cm as cm
from scipy.stats import norm
from matplotlib.colors import LogNorm
import numpy as np
import datetime as dt
import pandas as pd
import brewer2mpl as b2m

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
  retval = pd.DataFrame(data, columns = ['unix', 'freq'])
  retval['ts'] = pd.to_datetime(retval['unix'].astype(int), unit='s')
  retval['freq'] = retval['freq'].astype(float)
  retval['date'] = [c.date() for c in retval['ts']]
  retval['time'] = [c.time() for c in retval['ts']]
  min_ts = np.min(retval['ts'])
  #retval['d_since_start'] = [np.timedelta64(c, 'D').astype(int) for c in retval['ts'] - min_ts]
  min_unix = np.min(retval['unix'])
  #TODO: Skalierung ist kaputt. Siehe debug-output.
  daystart_offset = min_unix % (60*60*24)
  retval['d_since_start'] = ((retval['unix'] - (min_unix -
    daystart_offset) ) / (60*60*24)).astype(int)
  retval['s_since_midnight'] = [ c % (60*60*24) for c in retval['unix'] ]
  return retval

# Helper: convert seconds of day to HH:MM formatted string
def seconds_to_timeofday(seconds):
  hours = seconds/(60*60)
  sec=dt.timedelta(hours=hours)
  d=dt.datetime(2000,1,1) + sec
  retval = d.strftime("%H:%M")
  return retval

datasetfile = "datasets/20140723-export.txt"
print "loading ", datasetfile
df = load_data_as_dataframe(datasetfile)
print df.head()
min_day=np.min(df['d_since_start'])
max_day=np.max(df['d_since_start'])
print "Min day:", min_day
print "Max day:", max_day
minfreq = np.min(df['freq'])
maxfreq = np.max(df['freq'])
print "preparing data matrix"
datamatrix=np.zeros((24*60*60, max_day-min_day+1))
for i in range(len(df['freq'])):
  x = df['d_since_start'][i]
  y = df['s_since_midnight'][i]
  #print i, x, y
  datamatrix[y, x] = df['freq'][i]
#color_map = plt.cm.Spectral_r
color_map = b2m.brewer2mpl.get_map("Spectral", "Diverging",
    11).mpl_colormap
print "plotting."
p=plt.pcolormesh(datamatrix, 
    cmap=color_map,
    norm=LogNorm(vmin=np.min(df['freq']), vmax=np.max(df['freq']))
    )
freqticks = np.linspace(minfreq, maxfreq, 7)
ticklabels = ["%.3f" % s for s in freqticks]
cbar = plt.colorbar(p, spacing='log', ticks=freqticks)
cbar.ax.set_yticklabels(ticklabels)
cbar.set_label("Frequenz")
plt.ylim(0, 24*60*60)
#plt.xlim(0, max_day-min_day)
ylocs = np.arange(0, 24*60*60, 2*60*60)
ylocs, ylabels = plt.yticks(ylocs, 
    map(lambda y: seconds_to_timeofday(y), ylocs))
xlocs = np.arange(min_day, max_day+1, 1)
xlocs, xlabels = plt.xticks(xlocs,
    map(lambda x: x, xlocs))
    #verticalalignment = 'bottom')
#plt.setp(xlabels, rotation=45)
plt.ylabel("Uhrzeit (UTC)")
plt.xlabel("Tag")
plt.savefig("images/freq-heatmap.png", bbox_inches='tight')
