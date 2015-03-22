# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime as dt
import freqanalysis.datatools as datatool
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the HDF+ containing the frequency measurements")
args = cmd_parser.parse_args()

print "Reading from %s" % (args.datafile)

# Calculate the momentum (1st order derivative) of the frequency data
def add_freq_momentum(dataset):
  # First: Resample the dataset.
  dataset = dataset.set_index(pd.DatetimeIndex(dataset['ts']))
  dataset = dataset.resample("1min")
  # http://docs.scipy.org/doc/numpy/reference/generated/numpy.ediff1d.html#numpy.ediff1d
  momentum = np.ediff1d(dataset.freq, to_end=np.array([0]))
  #avgtimediff = np.mean(np.ediff1d(dataset.unix))
  dataset['momentum'] = momentum * 19500
  return dataset.dropna()

with pd.get_store(args.datafile) as store:
  eclipsedata = store['eclipsedata']
  fridaydata = store['fridaydata']
  print "Drawing solar eclipse frequency overview"
  f, ax = plt.subplots()
  lower_freq_limit = 49.95
  upper_freq_limit = 50.05
  ax.set_xlabel("Zeit [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  ax.set_ylim((lower_freq_limit, upper_freq_limit))
  ax.set_xlim((np.min(eclipsedata.time), np.max(eclipsedata.time)))
  ax.plot(eclipsedata.time, eclipsedata.freq, 'b', label="Netzfrequenz")
  ax.plot(ax.get_xlim(), (50.0, 50.0), 'r-', label="Sollwert")
  ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  f.suptitle("Sonnenfinsternis am 20.03.2015")
  f.autofmt_xdate()
  plt.savefig("images/sonnenfinsternis-frequenzverlauf.png")#, bbox_inches='tight')

  plt.clf()

  f, ax = plt.subplots(2)
  friday_momentum_df = add_freq_momentum(fridaydata)
  eclipse_momentum_df = add_freq_momentum(eclipsedata)
  lower_freq_limit = 49.95
  upper_freq_limit = 50.05
  ax[0].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[0].set_ylabel("Gradient [MW/min]")
  #ax[0].set_ylim((lower_freq_limit, upper_freq_limit))
  #ax[0].set_xlim((np.min(eclipsedata.time), np.max(eclipsedata.time)))
  ax[0].plot(eclipse_momentum_df.s_since_midnight.astype(int),
      eclipse_momentum_df.momentum, 'b.', label="Momentum")
  #ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[0].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[0].yaxis.set_major_formatter(y_formatter)
  ax[0].grid(True)

  ax[1].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[1].set_ylabel("Gradient [MW/min]")
  #ax[1].set_ylim((lower_freq_limit, upper_freq_limit))
  #ax[1].set_xlim((np.min(eclipsedata.time), np.max(eclipsedata.time)))
  ax[1].plot(friday_momentum_df.s_since_midnight.astype(int),
      friday_momentum_df.momentum, 'b.', label="Momentum")
  #ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[1].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[1].yaxis.set_major_formatter(y_formatter)
  ax[1].grid(True)

  f.suptitle("Sonnenfinsternis am 20.03.2015 - Leistungsgradienten")
  f.autofmt_xdate()
  plt.savefig("images/sonnenfinsternis-momentum.png")#, bbox_inches='tight')
