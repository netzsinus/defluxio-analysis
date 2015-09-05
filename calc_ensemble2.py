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

def add_freq_momentum(dataset):
  # First: Resample the dataset.
  #dataset2 = dataset.set_index(pd.DatetimeIndex(dataset.index))
  dataset2 = dataset.set_index(pd.to_datetime(dataset.index, unit='s',
      utc=True))

  dataset2 = dataset2.resample('1min')
  # http://docs.scipy.org/doc/numpy/reference/generated/numpy.ediff1d.html#numpy.ediff1d
  momentum = np.ediff1d(dataset2['freq']['mean'], to_end=np.array([0]))
  # Entso-E has published 19.5 GW/Hz
  dataset2['momentum'] = momentum * 19500
  return dataset2.dropna()

print "Reading from %s" % (args.datafile)
with pd.get_store(args.datafile) as store:
  alldata = store['alldata']
  print "Loaded dataset: ", alldata.shape


  ensemble = alldata.groupby('s_since_midnight').agg({'freq': [np.mean, np.min, np.max]})
  print ensemble.columns
  print "Calculating momentum"
  ensemble_momentum = add_freq_momentum(ensemble)
  # Recompute the unix timestamp explicitly, see http://stackoverflow.com/a/15203886
  ts = ensemble_momentum.index.astype(np.int64) // 10 ** 9
  ensemble_momentum['s_since_midnight'] = [ c % (60*60*24) for c in ts ]
  print ensemble_momentum.head()
  print "Saving the ensemble to data file %s" % args.datafile
  store['ensemble'] = ensemble
  store['ensemble_momentum'] = ensemble_momentum
  
