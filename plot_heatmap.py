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
import freqanalysis.datatools as datatool

datasetfile = "datasets/20140904-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)
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
ylocs = np.arange(0, 24*60*60, 60*60)
ylocs, ylabels = plt.yticks(ylocs, 
    map(lambda y: datatool.seconds_to_timeofday(y), ylocs))
xlocs = np.arange(min_day, max_day+1, 7)
xlocs, xlabels = plt.xticks(xlocs,
    map(lambda x: x, xlocs))
    #verticalalignment = 'bottom')
#plt.setp(xlabels, rotation=45)
plt.ylabel("Uhrzeit (UTC)")
plt.xlabel("Tag")
plt.savefig("images/freq-heatmap.png", bbox_inches='tight')
