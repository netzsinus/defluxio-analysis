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
import freqanalysis.event as event


datasetfile = "datasets/20140728-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)

abs_deviation_mHz = 70
print "Looking for absolute deviations above ", abs_deviation_mHz

pos_df = event.filter_absolute_positive_deviation(df, abs_deviation_mHz)
print "found ", len(pos_df), " absolute positive deviations"

neg_df = event.filter_absolute_negative_deviation(df, abs_deviation_mHz)
print "found ", len(neg_df), " absolute negative deviations"


###
## Plotting the readings violating the threshold.
#
minfreq = np.min(df['freq'])
maxfreq = np.max(df['freq'])
print "preparing data matrix"
deviations=np.zeros((60, 24))
for i in pos_df.index:
  if deviations[pos_df['minute'][i], pos_df['hour'][i]] == 0:
    deviations[pos_df['minute'][i], pos_df['hour'][i]] = pos_df['freq'][i]
  else:
    deviations[pos_df['minute'][i], pos_df['hour'][i]] = \
      max(deviations[pos_df['minute'][i], pos_df['hour'][i]], pos_df['freq'][i])
for i in neg_df.index:
  if deviations[neg_df['minute'][i], neg_df['hour'][i]] == 0:
      deviations[neg_df['minute'][i], neg_df['hour'][i]] = neg_df['freq'][i]
  else:
    deviations[neg_df['minute'][i], neg_df['hour'][i]] = \
      min(deviations[neg_df['minute'][i], neg_df['hour'][i]], neg_df['freq'][i])
##color_map = plt.cm.Spectral_r
color_map = b2m.brewer2mpl.get_map("Spectral", "Diverging",
    11).mpl_colormap
print "plotting: Maximale Abweichung/Uhrzeit."
p=plt.pcolormesh(deviations, 
    cmap=color_map,
    norm=LogNorm(vmin=np.min(df['freq']), vmax=np.max(df['freq']))
    )
freqticks = np.linspace(minfreq, maxfreq, 7)
ticklabels = ["%.3f" % s for s in freqticks]
cbar = plt.colorbar(p, spacing='log', ticks=freqticks)
cbar.ax.set_yticklabels(ticklabels)
cbar.set_label("Frequenz")
plt.ylim(0, 59)
plt.xlim(0, 23)
plt.ylabel("Minute")
plt.xlabel("Stunde")
plt.title("Maximale Abweichung nach Uhrzeit")
plt.savefig("images/deviation-frequency-heatmap.png", bbox_inches='tight')

plt.clf()
###
## Plotting the amount of readings violating the threshold.
#
minfreq = np.min(df['freq'])
maxfreq = np.max(df['freq'])
print "preparing data matrix"
deviations=np.zeros((60, 24))
for i in pos_df.index:
  deviations[pos_df['minute'][i], pos_df['hour'][i]] = \
    deviations[pos_df['minute'][i], pos_df['hour'][i]] + 1
for i in neg_df.index:
  deviations[neg_df['minute'][i], neg_df['hour'][i]] = \
    deviations[neg_df['minute'][i], neg_df['hour'][i]] + 1
color_map = b2m.brewer2mpl.get_map("Reds", "Sequential",
    9).mpl_colormap
print "plotting: Anzahl Abweichungen/Uhrzeit."
p=plt.pcolormesh(deviations, 
    cmap=color_map
    #norm=LogNorm(vmin=np.min(deviations), vmax=np.max(deviations))
    )
cbar = plt.colorbar(p, spacing='log')#, ticks=freqticks)
cbar.set_label("Anzahl")
plt.ylim(0, 59)
plt.xlim(0, 23)
plt.ylabel("Minute")
plt.xlabel("Stunde")
plt.title("Anzahl Abweichungen nach Uhrzeit")
plt.savefig("images/deviation-occurence-heatmap.png", bbox_inches='tight')
