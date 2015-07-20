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

with pd.get_store(args.datafile) as store:
  all = store['alldata']
  minfreq = np.min(all['freq'])
  maxfreq = np.max(all['freq'])
  print "Frequency: Min=%.3f, Max=%.3f" % (minfreq, maxfreq)
