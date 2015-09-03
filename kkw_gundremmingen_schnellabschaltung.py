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
import freqanalysis.graphtools as gt
import scipy.signal as sig
from scipy import stats
import math
import argparse

# Global parameters
starttime = 1427268883
bottomtime = 1427268902
startfreq = 49.996
bottomfreq = 49.948
setfreq = 50.0
delta_f2=bottomfreq - setfreq
delta_Pa = -1290


cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the HDF+ containing the frequency measurements")
args = cmd_parser.parse_args()

print "Reading from %s" % (args.datafile)

with pd.get_store(args.datafile) as store:
  grundremmingen = store['grundremmingen']
  #TODO: Move these timestamps to stagedata.py
  #grundremmingen = grundremmingen[(grundremmingen.unix >= 1427268780) &
  #    (grundremmingen.unix < 1427269200)]

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
  ax.plot(grundremmingen.time, grundremmingen.freq, 'b-', label=r"Netzfrequenz")
  #ax.plot(grundremmingen.time, grundremmingen.freq_sg, 'b', label=r"Netzfrequenz")
  trumpet = datatool.calc_trumpet_curve(starttime, setfreq, startfreq, bottomfreq
      - startfreq, delta_Pa)
  ax.plot(trumpet.time, trumpet.trumpneg, 'r', label=r"Trompetenkurve")
  half_trumpet = 50 - (50-trumpet.trumpneg) / 2.0
  ax.plot(trumpet.time, half_trumpet, 'y', label=r"$50\%$ Trompetenkurve")
  ax.plot(ax.get_xlim(), (setfreq, setfreq), 'b--', label=r"Sollwert $f_0 = 50Hz$")

  print "Beginn der Schnellabschaltung um %s bei %.3f Hz" % (datatool.unix2time(starttime), startfreq)
  gt.draw_target_cross(ax, starttime, startfreq, r"Schnellabschaltung $f_1=%.3f$" % startfreq)
  
  print "Tiefpunkt der Frequenz um %s bei %.3f Hz" % (datatool.unix2time(bottomtime), bottomfreq)
  gt.draw_target_cross(ax, bottomtime, bottomfreq, 
    r"Tiefstand $f_2=%.3f$" % bottomfreq)

  ax.legend(loc="best", ncol=2, fontsize="small")
  ax.text(0.95, 0.01, r'$\Delta f_2=52 mHz$, $\Delta t = 19 s$',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes)
  #ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
  #         ncol=2, mode="expand", borderaxespad=0.)
  #hfmt = dates.DateFormatter('%H:%M')
  #ax.xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  f.suptitle(r"Schnellabschaltung KKW Gundremmingen 25.03.2015, $\Delta P_a = -1290MW$")
  f.autofmt_xdate()
  plt.savefig("images/gundremmingen-frequenzverlauf.png")#, bbox_inches='tight')
  plt.clf()

  print "Drawing momentum graph"
  f, ax = plt.subplots(2)
  grundremmingen_momentum_df = datatool.resample_add_freq_momentum(grundremmingen, 19000)
  lower_momentum_limit = np.min(grundremmingen_momentum_df.momentum)
  upper_momentum_limit = np.max(grundremmingen_momentum_df.momentum)

  ax[0].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[0].set_ylabel("Frequenz [Hz]")
  ax[0].set_xlim((np.min(grundremmingen_momentum_df.s_since_midnight.astype(int)), 
    np.max(grundremmingen_momentum_df.s_since_midnight.astype(int))))
  ax[0].plot(grundremmingen_momentum_df.s_since_midnight.astype(int),
      grundremmingen_momentum_df.freq, 'r', label=r"Frequenzmessung")
  ax[0].plot(grundremmingen_momentum_df.s_since_midnight.astype(int),
      grundremmingen_momentum_df.freq_sg, 'b', label=r"Savitzky-Golay (7, 2)")
  ax[0].legend(loc="lower right", fontsize="small")
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[1].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[0].yaxis.set_major_formatter(y_formatter)
  ax[0].grid(True)

  ax[1].set_xlabel("Zeit [Sekunden seit Mitternacht UTC]")
  ax[1].set_ylabel("Gradient [MW/min]")
  ax[1].set_ylim((lower_momentum_limit, upper_momentum_limit))
  ax[1].set_xlim((np.min(grundremmingen_momentum_df.s_since_midnight.astype(int)), 
    np.max(grundremmingen_momentum_df.s_since_midnight.astype(int))))
  ax[1].plot(grundremmingen_momentum_df.s_since_midnight.astype(int),
      grundremmingen_momentum_df.momentum, 'r-', label="Momentum")
  #ax.legend()
  #hfmt = dates.DateFormatter('%H:%M')
  #ax[0].xaxis.set_major_formatter(hfmt)
  y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
  ax[1].yaxis.set_major_formatter(y_formatter)
  ax[1].grid(True)

  f.suptitle("Schnellabschaltung KKW Gundremmingen 25.03.2015 - Leistungsgradienten")
  f.autofmt_xdate()
  plt.savefig("images/gundremmingen-gradienten.png")#, bbox_inches='tight')


