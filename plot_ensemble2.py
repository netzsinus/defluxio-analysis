# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime as dt
import freqanalysis.datatools as datatool
import argparse
from matplotlib.ticker import AutoMinorLocator

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="HDF+ file containing the ensemble data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.datafile)
with pd.get_store(args.datafile) as store:
  ensemble = store['ensemble']
  
  min_quantile = 0.0005
  max_quantile = 0.9999
  quantiles = ensemble.quantile([min_quantile, max_quantile])
  print "Quantiles are:"
  print quantiles
  minimum_cutoff = quantiles['freq']['amin'].iloc[0]
  maximum_cutoff = quantiles['freq']['amax'].iloc[1]
  print "Using cutoffs: min = %.4f, max=%.4f" % (minimum_cutoff,
      maximum_cutoff)

  ensemble_filtered = ensemble[(ensemble['freq']['amin'] >
      minimum_cutoff) & (ensemble['freq']['amax'] <
      maximum_cutoff)]

  print "Drawing 24h overview"
  fig, ax = plt.subplots(figsize=(16, 9), dpi=75)
  ax.set_title("Ensemble der Netzfrequenz")
  ax.set_xlabel("Stunde [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  # format the ticks & enable the grid
  hours = mdates.HourLocator()
  minutes   = mdates.MinuteLocator()
  hoursFmt = mdates.DateFormatter('%H')
  ax.xaxis.set_major_locator(hours)
  ax.xaxis.set_major_formatter(hoursFmt)
  ax.xaxis.set_minor_locator(minutes)
  ax.grid(True, which='both')
  # reconstruct the time index
  ts = pd.to_datetime(ensemble_filtered.index, unit='s')
  ax.fill_between(ts, ensemble_filtered['freq','amin'],
      ensemble_filtered['freq', 'amax'], color='grey', alpha='0.5',
      label="Wertebereich (0.001-0.999)-Quantil")
  # reconstruct the time index
  ts = pd.to_datetime(ensemble.index, unit='s')
  ax.plot(ts, ensemble['freq','mean'], 'k', label="Mittlere Netzfrequenz")
  p1 = plt.Line2D((0, 0), (1, 1), linewidth=2, color="black")
  p2 = plt.Rectangle((0, 0), 1, 1, fc="grey")
  ax.legend([p1, p2], ['Mittlere Netzfrequenz', "(%.4f-%.4f)-Quantil" %
    (min_quantile, max_quantile)])
  plt.tight_layout()
  plt.savefig("images/frequenz-ensemble2.png", bbox_inches='tight')

  print "Drawing evening subplot overview"
  mintime = 18*60*60
  maxtime = 23*60*60
  ensemble = ensemble[(ensemble.index > mintime) & (ensemble.index <
    maxtime)]
  ensemble_filtered= ensemble_filtered[(ensemble_filtered.index >
    mintime) & (ensemble_filtered.index < maxtime)]
  plt.clf()
  fig, ax = plt.subplots(figsize=(16, 9), dpi=75)
  ax.set_title("Ensemble der Netzfrequenz (18:00-23:00)")
  ax.set_xlabel("Stunde [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  # format the ticks & enable the grid
  hours = mdates.HourLocator()
  #minutes   = mdates.MinuteLocator()
  minutes = AutoMinorLocator(4)
  hoursFmt = mdates.DateFormatter('%H:%M')
  ax.xaxis.set_major_locator(hours)
  ax.xaxis.set_major_formatter(hoursFmt)
  ax.xaxis.set_minor_locator(minutes)
  ax.grid(True, which='both')
  # reconstruct the time index
  ts = pd.to_datetime(ensemble_filtered.index, unit='s')
  ax.fill_between(ts, ensemble_filtered['freq','amin'],
      ensemble_filtered['freq', 'amax'], color='grey', alpha='0.5',
      label="Wertebereich (0.001-0.999)-Quantil")
  # reconstruct the time index
  ts = pd.to_datetime(ensemble.index, unit='s')
  ax.plot(ts, ensemble['freq','mean'], 'k', label="Mittlere Netzfrequenz")
  p1 = plt.Line2D((0, 0), (1, 1), linewidth=2, color="black")
  p2 = plt.Rectangle((0, 0), 1, 1, fc="grey")
  ax.legend([p1, p2], ['Mittlere Netzfrequenz', "(%.4f-%.4f)-Quantil" %
    (min_quantile, max_quantile)])
  plt.tight_layout()
  plt.savefig("images/frequenz-ensemble-evening.png", bbox_inches='tight')

