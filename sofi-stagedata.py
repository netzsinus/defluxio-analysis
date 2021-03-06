import pandas as pd
import freqanalysis.datatools as datatool
import numpy as np
import sys as sys
import argparse
import os

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the csv containing the frequency measurements")
cmd_parser.add_argument("outfile", help="HDF+ file to create")
args = cmd_parser.parse_args()

print "Slurping the CSV-file %s, writing to %s" % (args.datafile,
    args.outfile)

print "Loading datasets. This might take a while."
alldata = datatool.load_data_as_dataframe(args.datafile)

print "Selecting all friday data for comparison."
# select the friday 8:00 to 11:00 UTC datasets from the alldata frame
fridays = alldata[alldata.weekday == 4]
fridaydata = fridays[(fridays.hour > 7) & (fridays.hour < 11)]

print "Selecting eclipse data"
eclipsedata = alldata[(alldata.unix >= 1426838400) & (alldata.unix < 1426849200)]

with pd.get_store(args.outfile) as store:
  store['eclipsedata'] = eclipsedata
  store['fridaydata'] = fridaydata


