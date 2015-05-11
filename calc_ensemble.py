import pandas as pd
import freqanalysis.datatools as datatool
import numpy as np
import sys as sys
import argparse
# pip install progressbar2
import progressbar as pb
import os

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datadir", help="directory containing the frequency measurements (i.e. YYYYMMDD.txt files)")
cmd_parser.add_argument("outfile", help="HDF+ file to add ensemble data to")
args = cmd_parser.parse_args()

print "Slurping data from %s, writing to %s" % (args.datadir,
    args.outfile)
files = sorted(os.listdir(args.datadir))

print "Iterating over datasets. This might take a while."
ensemble_all = np.empty([datatool.secs_per_day()])
counter_all = np.empty([datatool.secs_per_day()])
ensemble_weekend = np.empty([datatool.secs_per_day()])
counter_weekend = np.empty([datatool.secs_per_day()])
ensemble_weekday = np.empty([datatool.secs_per_day()])
counter_weekday = np.empty([datatool.secs_per_day()])
with pb.ProgressBar(maxval=len(files)) as progress:
  for idx, file in enumerate(files):
    freqdata = datatool.load_data_as_dataframe(os.path.join(args.datadir, file))
    weekend = False
    if freqdata.iloc[0].weekday in set([5, 6]):
      weekend = True
    for i, row in freqdata.iterrows():
      ensemble_all[row.s_since_midnight] += row.freq
      counter_all[row.s_since_midnight] += 1
      if weekend:
        ensemble_weekend[row.s_since_midnight] += row.freq
        counter_weekend[row.s_since_midnight] += 1
      else:
        ensemble_weekday[row.s_since_midnight] += row.freq
        counter_weekday[row.s_since_midnight] += 1
    progress.update(idx)

ensemble_all = ensemble_all / counter_all
ensemble_weekend = ensemble_weekend / counter_weekend
ensemble_weekday = ensemble_weekday / counter_weekday
print "Saving computed ensemble"
with pd.get_store(args.outfile) as store:
  ensemble_all_df = pd.DataFrame({
      's_since_midnight': np.arange(0, datatool.secs_per_day(), 1),
      'freq': ensemble_all
    })
  store['ensemble_all'] = ensemble_all_df
  ensemble_weekend_df = pd.DataFrame({
      's_since_midnight': np.arange(0, datatool.secs_per_day(), 1),
      'freq': ensemble_weekend
    })
  store['ensemble_weekend'] = ensemble_weekend_df
  ensemble_weekday_df = pd.DataFrame({
      's_since_midnight': np.arange(0, datatool.secs_per_day(), 1),
      'freq': ensemble_weekday
    })
  store['ensemble_weekday'] = ensemble_weekday_df







