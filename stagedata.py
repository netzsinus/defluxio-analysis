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
print "Computing Savitzky-Golay Filter (windowlen=7, polyorder=2)"
alldata['freq_sg'] = sig.savgol_filter(alldata['freq'], 7, 2)

#print "Selecting all friday data for comparison."
## select the friday 8:00 to 11:00 UTC datasets from the alldata frame
fridaydata = alldata[(alldata.weekday == 4) & (alldata.hour > 7) &
    (alldata.hour < 11)]

print "Selecting eclipse data"
eclipsedata = alldata[(alldata.unix >= 1426838400) & (alldata.unix < 1426849200)]

print "Selecting KKW Grundremmingen Schnellabschaltung 25.03.2015 data"
grundremmingen = alldata[(alldata.unix >= 1427268780) & (alldata.unix < 1427269200)]

with pd.get_store(args.outfile) as store:
  store['eclipsedata'] = eclipsedata
  store['fridaydata'] = fridaydata
  store['grundremmingen'] = grundremmingen


