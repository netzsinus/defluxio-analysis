# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import datetime as dt
import freqanalysis.datatools as datatool
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="HDF+ file containing the ensemble data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.datafile)
with pd.get_store(args.datafile) as store:
  ensemble_all_df = store['ensemble_all']
  ensemble_weekday_df = store['ensemble_weekday']
  ensemble_weekend_df = store['ensemble_weekend']
  print "Calculating Savitzky-Golay filter (2nd degree polynom, window length 7)"
  datatool.addSavitzkyGolay(ensemble_all_df)
  datatool.addSavitzkyGolay(ensemble_weekday_df)
  datatool.addSavitzkyGolay(ensemble_weekend_df)
  print "Drawing"
  mintime = np.min(ensemble_all_df['s_since_midnight'])
  maxtime = np.max(ensemble_all_df['s_since_midnight'])
  plt.title("Ensemble der Netzfrequenz")
  plt.xlabel("Zeit [UTC]")
  plt.ylabel("Frequenz [Hz]")
  #plt.plot(ensemble_all_df.s_since_midnight,
  #    ensemble_all_df.freq_sg, 'k', label="Alle Tage")
  plt.plot(ensemble_weekday_df.s_since_midnight,
      ensemble_weekday_df.freq_sg, 'b', label="Wochentag")
  plt.plot(ensemble_weekend_df.s_since_midnight,
      ensemble_weekend_df.freq_sg, 'r', label="Wochenende")
  xlocs = np.arange(mintime, maxtime, 60*60)
  xlocs, xlabels = plt.xticks(xlocs, 
        map(lambda x: datatool.seconds_to_timeofday(x), xlocs))
  plt.setp(xlabels, rotation=45)
  plt.grid(True, which='both')
  plt.legend(loc="best", fontsize="small")

  plt.xlim(0, 60*60*24-1)
 

  #plt.legend()
  #axarr[0].plot(axarr[0].get_xlim(), (lower_freq_limit, lower_freq_limit), 'r-')
  #axarr[0].plot(axarr[0].get_xlim(), (upper_freq_limit, upper_freq_limit), 'r-')

  ## the histogram of the data
  #n, bins, patches = axarr[1].hist(diofreq, 100, normed=1, facecolor='green', alpha=0.75)
  ## add a 'best fit' line
  #y = mlab.normpdf( bins, mu, sigma)
  #l = axarr[1].plot(bins, y, 'r--', linewidth=1)
  #axarr[1].set_xlabel('Frequenz [Hz]')
  #axarr[1].set_ylabel(u'Häufigkeit')
  #axarr[1].set_title(r'$\mathrm{Histogram\ der\ Frequenz:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
  #
  ## add 3sigma lines to the plots
  #axarr[1].plot((lower_freq_limit, lower_freq_limit),
  #    axarr[1].get_ylim(), 'r-')
  #axarr[1].plot((upper_freq_limit, upper_freq_limit),
  #    axarr[1].get_ylim(), 'r-')
  #axarr[1].grid(True)
  #
plt.tight_layout()
plt.savefig("images/frequenz-ensemble.png", bbox_inches='tight')

