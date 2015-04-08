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

# Global parameters
starttime = 1427268883
bottomtime = 1427268902
startfreq = 49.996
bottomfreq = 49.948

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
  grundremmingen = grundremmingen[(grundremmingen.unix >= 1427268780) &
      (grundremmingen.unix < 1427269200)]

  print "Drawing Schnellabschaltung overview"
  f, ax = plt.subplots()
  lower_freq_limit = 49.94
  upper_freq_limit = 50.025
  ax.set_xlabel("Zeit [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  ylim = (lower_freq_limit, upper_freq_limit)
  ax.set_ylim(ylim)
  xlim = (np.min(grundremmingen.time), np.max(grundremmingen.time))
  ax.set_xlim(xlim)
  ax.plot(grundremmingen.time, grundremmingen.freq, 'b', label="Netzfrequenz")
  ax.plot(ax.get_xlim(), (50.0, 50.0), 'b--', label="Sollwert")

  print "Beginn der Schnellabschaltung um %s bei %.3f Hz" % (datatool.unix2time(starttime), startfreq)
  begin_time_line = (datatool.unix2time(starttime),
    datatool.unix2time(starttime))
  ax.plot(begin_time_line, ylim, 'r--', label="Schnellabschaltung")
  begin_freq_line = (startfreq, startfreq)
  ax.plot(xlim, begin_freq_line, 'r--')

  print "Tiefpunkt der Frequenz um %s bei %.3f Hz" % (datatool.unix2time(bottomtime), bottomfreq)
  bottom_time_line = (datatool.unix2time(bottomtime),
    datatool.unix2time(bottomtime))
  ax.plot(bottom_time_line, ylim, 'r-.', label="Tiefstand")
  bottom_freq_line = (bottomfreq, bottomfreq)
  ax.plot(xlim, bottom_freq_line, 'r-.')

  ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  f.suptitle("Schnellabschaltung KKW Grundremmingen 25.03.2015")
  f.autofmt_xdate()
  #plt.savefig("images/grundremmingen-frequenzverlauf.png")#, bbox_inches='tight')
  plt.show()
