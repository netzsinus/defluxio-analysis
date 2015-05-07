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
ensemble = np.empty([datatool.secs_per_day()])
counter = np.empty([datatool.secs_per_day()])
with pb.ProgressBar(maxval=len(files)) as progress:
  for idx, file in enumerate(files):
    freqdata = datatool.load_data_as_dataframe(os.path.join(args.datadir, file))
    for i, row in freqdata.iterrows():
      ensemble[row.s_since_midnight] += row.freq
      counter[row.s_since_midnight] += 1
    progress.update(idx)

ensemble = ensemble / counter
print "Saving computed ensemble"
with pd.get_store(args.outfile) as store:
  ensemble_df = TODO!
  store['ensemble'] = ensemble_df



