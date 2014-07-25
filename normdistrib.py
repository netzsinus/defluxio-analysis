# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import freqanalysis.datatools as datatool
import freqanalysis.normdist as nd



datasetfile = "datasets/20140723-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)
df['minute'] = df.time.apply(lambda x: x.minute)
hour_df = df[(df.minute >= 58) | (df.minute <= 3)]

f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
# pandas/matplotlib incompatibility: http://stackoverflow.com/a/22764377
nd.plot_fit(df['freq'].values, ax1, "Alle Werte")
nd.plot_fit(hour_df['freq'].values, ax2, "Nur Stundenwechsel:")

f.savefig("images/normdistrib.png", bbox_inches='tight')



