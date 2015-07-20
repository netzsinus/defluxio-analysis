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

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the HDF+ containing the frequency measurements")
args = cmd_parser.parse_args()

print "Reading from %s" % (args.datafile)
print "not working - see https://blog.stromhaltig.de/2013/10/die-netzzeit-wenn-50-hz-aus-dem-takt-geraet/ for another approach"

with pd.get_store(args.datafile) as store:
  all = store['alldata']
  print "Computing rolling mean"
  rollingmean = pd.rolling_mean(all['freq'], 60*60)
  if np.any(rollingmean > 50.010) or np.any(rollingmean < 49.990):
    print "Zeitkorrektur!"
  print "Rolling mean freq: min=%.3f, max=%.3f, mean=%.3f" % \
    (np.min(rollingmean), np.max(rollingmean), np.mean(rollingmean))
  plt.plot(rollingmean)
  plt.show()
