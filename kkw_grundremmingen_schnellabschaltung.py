# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime as dt
import freqanalysis.datatools as datatool
import freqanalysis.ecdf as ecdf
from scipy import stats
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
  # Entso-E has published 19.5 GW/Hz
  dataset['momentum'] = momentum * 19500
  return dataset.dropna()

with pd.get_store(args.datafile) as store:
  grundremmingen = store['grundremmingen']

  print "Drawing Schnellabschaltung overview"
  f, ax = plt.subplots()
  lower_freq_limit = 49.9
  upper_freq_limit = 50.1
  ax.set_xlabel("Zeit [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  ax.set_ylim((lower_freq_limit, upper_freq_limit))
  ax.set_xlim((np.min(grundremmingen.time), np.max(grundremmingen.time)))
  ax.plot(grundremmingen.time, grundremmingen.freq, 'b', label="Netzfrequenz")
  ax.plot(ax.get_xlim(), (50.0, 50.0), 'r-', label="Sollwert")
  ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  f.suptitle("Schnellabschaltung KKW Grundremmingen 25.03.2015")
  f.autofmt_xdate()
  plt.savefig("images/grundremmingen-frequenzverlauf.png")#, bbox_inches='tight')
