# vim:fileencoding=utf-8
import numpy as np
import pandas as pd
import datetime as dt
import freqanalysis.datatools as datatool
import freqanalysis.ecdf as ecdf
import freqanalysis.graphtools as gt
import math
import argparse


cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the HDF+ containing the frequency measurements")
args = cmd_parser.parse_args()

print "Reading from %s" % (args.datafile)

with pd.get_store(args.datafile) as store:
  alldata = store['alldata']
  print alldata.head()
  print alldata.shape

  ensemble = alldata.groupby('s_since_midnight').agg({'freq': [np.mean, np.min, np.max]})
  # The dailyfreq dataframe has a multiindex. Inspect it by uncommenting the following line:
  print ensemble.columns
  print "Saving the ensemble to data file %s" % args.datafile
  store['ensemble'] = ensemble
  
