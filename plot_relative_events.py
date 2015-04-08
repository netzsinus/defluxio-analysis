# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import freqanalysis.datatools as datatool
import freqanalysis.event as event


datasetfile = "datasets/20140904-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)

rel_deviation_Hz = 0.14
window_num_minutes = 10
window_num_seconds = 60 * window_num_minutes
print "Looking for relative deviations above ", rel_deviation_Hz
print "Using window of size", window_num_seconds, "seconds"

min_ts = np.min(df['unix'])
max_ts = np.max(df['unix'])
half_window_size = window_num_seconds/2
quarter_window_size = window_num_seconds/4

event_id = 0
for i in np.arange(min_ts + half_window_size, max_ts - half_window_size,
    quarter_window_size):
  window = df[(df.unix >= i-half_window_size) & (df.unix <
    i+half_window_size)]
  max_deviation = np.max(window['freq']) - np.min(window['freq'])
  if max_deviation > (rel_deviation_Hz):
    fulldatestring = "%s %s (UTC)" % (datatool.seconds_to_date(i),
        datatool.seconds_to_timeofday(i))
    title_string = "%s: %.3f Hz" % (fulldatestring, max_deviation)
    file_string = "(%d) - %s - %f" % (event_id, datatool.seconds_to_date(i), max_deviation)
    print "Found deviation: ", title_string
    plt.clf()
    plt.title("%s" % title_string)
    plt.xlabel("Uhrzeit")
    plt.ylabel("Frequenz [Hz]")
    plt.plot(window['unix'], window['freq'], 'r')
    plt.xlim(np.min(window['unix']), np.max(window['unix']))
    xlocs = np.arange(np.min(window['unix']), np.max(window['unix']), 60)
    xlocs, xlabels = plt.xticks(xlocs, 
        map(lambda x: datatool.seconds_to_timeofday(x), xlocs))
    plt.setp(xlabels, rotation=45)
    plt.savefig("images/events/%s.png" % file_string, bbox_inches='tight')
    event_id = event_id + 1






