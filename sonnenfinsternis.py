# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator
import matplotlib.patches as patches
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
  eclipsedata = store['eclipsedata']
  fridaydata = store['fridaydata']
  ensemble = store['ensemble']
  ensemble_momentum = store['ensemble_momentum']
  friday_momentum_df = add_freq_momentum(fridaydata)
  eclipse_momentum_df = add_freq_momentum(eclipsedata)
  #TODO: The structure of the ensemble is different. Needs to be
  #adjusted.
  #ensemble_momentum_df = add_freq_momentum(ensemble)

  print "Drawing solar eclipse frequency overview"
  f, ax = plt.subplots(figsize=(16, 9), dpi=75)
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


  print "Drawing solar eclipse frequency comparison"
  plt.clf()
  f, ax = plt.subplots(figsize=(16, 9), dpi=75)
  eclipsestart = np.min(eclipsedata.s_since_midnight)
  eclipseend = np.max(eclipsedata.s_since_midnight)
  ensemble = ensemble[(ensemble.index >= eclipsestart) & 
      (ensemble.index <= eclipseend)]
  ax.set_xlabel("Zeit [UTC]")
  ax.set_ylabel("Frequenz [Hz]")
  #ax.set_xlim((eclipsestart, eclipseend))
  ts = pd.to_datetime(eclipsedata.s_since_midnight, unit='s')
  ax.plot(ts, eclipsedata.freq, 'b', label="Netzfrequenz Sonnenfinsternis")
  ts = pd.to_datetime(ensemble.index.to_series(), unit='s')
  ax.plot(ts, ensemble['freq','mean'], 'r', label="Mittlere Netzfrequenz")

  ax.add_patch(
      patches.Rectangle(
          (eclipsestart, 49.98),   # (x,y)
          eclipseend-eclipsestart,          # width
          0.04,          # height
      )
  )

  #ax.plot(ax.get_xlim(), (50.0, 50.0), 'r-', label="Sollwert")
  ax.legend()
# format the ticks & enable the grid
  #hours = dates.HourLocator()
  #minutes   = dates.MinuteLocator()
  #hoursFmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_locator(hours)
  #ax.xaxis.set_major_formatter(hoursFmt)
  #ax.xaxis.set_minor_locator(minutes)

  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True, which='both')

  f.suptitle("Sonnenfinsternis am 20.03.2015")
  plt.savefig("images/sonnenfinsternis-frequenzverlauf-vergleich.png")#, bbox_inches='tight')

  plt.clf()
  f, ax = plt.subplots(2, figsize=(16, 9), dpi=75)
  lower_momentum_limit = np.min(friday_momentum_df.momentum)
  upper_momentum_limit = np.max(friday_momentum_df.momentum)
  ax[0].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[0].set_ylabel("Gradient [MW/min]")
  ax[0].set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax[0].set_xlim((np.min(eclipse_momentum_df.s_since_midnight.astype(int)), 
    np.max(eclipse_momentum_df.s_since_midnight.astype(int))))
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
  ax[1].set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax[1].set_xlim((np.min(eclipse_momentum_df.s_since_midnight.astype(int)), 
    np.max(eclipse_momentum_df.s_since_midnight.astype(int))))
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
  plt.savefig("images/sonnenfinsternis-gradienten.png")#, bbox_inches='tight')

  plt.clf()
  f, ax = plt.subplots(1, figsize=(16, 9), dpi=75)
  lower_momentum_limit = np.min(eclipse_momentum_df.momentum)
  upper_momentum_limit = np.max(eclipse_momentum_df.momentum)
  mintime = np.min(eclipse_momentum_df.s_since_midnight.astype(int))
  maxtime = np.max(eclipse_momentum_df.s_since_midnight.astype(int))
  ax.set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax.set_ylabel("Gradient [MW/min]")
  ax.set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax.set_xlim((mintime, maxtime))
  ax.plot(ensemble_momentum.s_since_midnight.astype(int),
      ensemble_momentum.momentum, 'r', linewidth=2,
      label="Ensemble-Leistungsgradient")
  ax.plot(eclipse_momentum_df.s_since_midnight.astype(int),
    eclipse_momentum_df.momentum, 'b-', label="Leistungsgradient SoFi", linewidth=2)
  ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[0].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)
  f.suptitle("Sonnenfinsternis am 20.03.2015 - Leistungsgradienten")
  f.autofmt_xdate()
  plt.savefig("images/sonnenfinsternis-ensemble-gradienten.png", bbox_inches='tight')


  plt.clf()
  f, ax = plt.subplots(2, figsize=(16, 9), dpi=75)
  lower_momentum_limit = np.min(ensemble_momentum.momentum)
  upper_momentum_limit = np.max(ensemble_momentum.momentum)
  mintime = np.min(eclipse_momentum_df.s_since_midnight.astype(int))
  maxtime = np.max(eclipse_momentum_df.s_since_midnight.astype(int))
  ax[0].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[0].set_ylabel("Gradient [MW/min]")
  ax[0].set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax[0].set_xlim((mintime, maxtime))
  ax[0].plot(eclipse_momentum_df.s_since_midnight.astype(int),
      eclipse_momentum_df.momentum, 'b-', label="Leistungsgradient SoFi")
  ax[0].legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[0].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[0].yaxis.set_major_formatter(y_formatter)
  ax[0].grid(True)

  ax[1].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[1].set_ylabel("Gradient [MW/min]")
  ax[1].set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax[1].set_xlim((mintime, maxtime))
  ax[1].plot(ensemble_momentum.s_since_midnight.astype(int),
      ensemble_momentum.momentum, 'k',
      label="Ensemble-Leistungsgradient")
  ax[1].legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[1].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[1].yaxis.set_major_formatter(y_formatter)
  ax[1].grid(True)

  f.suptitle("Sonnenfinsternis am 20.03.2015 - Leistungsgradienten")
  f.autofmt_xdate()
  plt.savefig("images/sonnenfinsternis-ensemble-gradienten2.png")#, bbox_inches='tight')



  plt.clf()
  lower_freq_limit = 49.95
  upper_freq_limit = 50.05
  plt.xlabel("Zeit [UTC]")
  plt.ylabel("Gradient [MW/min]")
  plt.hexbin(friday_momentum_df.s_since_midnight.astype(int),
      friday_momentum_df.momentum, gridsize=80, cmap=cm.Reds)
  cp=plt.colorbar()
  cp.set_label(u"Häufigkeit")
  #plt.plot(eclipse_momentum_df.s_since_midnight.astype(int),
  #    eclipse_momentum_df.momentum, 'r-', label="Momentum")

  #hfmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_formatter(hfmt)
#  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
#  ax.yaxis.set_major_formatter(y_formatter)
#  ax.grid(True)

  f.suptitle("Dichte der Leistungsgradienten")
  f.autofmt_xdate()
  plt.savefig("images/sonnenfinsternis-dichte-gradienten.png")#, bbox_inches='tight')

  plt.clf()
  friday_series, friday_vals = ecdf.get_ecdf(friday_momentum_df.momentum)
  ecdf.plot_ecdf_curve(friday_series, friday_vals, color="b", label="Typischer Freitag")
  eclipse_series, eclipse_vals = ecdf.get_ecdf(eclipse_momentum_df.momentum)
  ecdf.plot_ecdf_curve(eclipse_series, eclipse_vals, color="r", label="Sonnenfinsternis")
  print "Mittelwert alle Freitage: %f" % np.median(friday_momentum_df.momentum)
  print "Mittelwert Sonnenfinsternis: %f" % np.median(eclipse_momentum_df.momentum)
  # http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html#scipy.stats.levene
  W, p_val = stats.levene(friday_momentum_df.momentum,
      eclipse_momentum_df.momentum, center='median')
  print ("Levenes Test auf Gleichheit der Varianz: P=%s (gleiche Varianz für p<=0.05)" % p_val)


  W, p_val = stats.fligner(friday_momentum_df.momentum, eclipse_momentum_df.momentum)
  print "Fliegners Test auf Gleichheit der Varianz: P=%s" % p_val

  f.suptitle("ECDF der Leistungsgradienten: Ungleiche Varianzen (Levene, p=%f)" % p_val)
  plt.savefig("images/sonnenfinsternis-ecdf-gradienten.png")#, bbox_inches='tight')

 
