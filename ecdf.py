# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import freqanalysis.ecdf as ecdf
import freqanalysis.datatools as datatool



datasetfile = "datasets/20140723-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)
print df.head()
print "Calculating ECDF"
# todo: filter ECDF based on time (mid-hour vs. hour-change)
# see http://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
# df['time'].minute > 55 | df['time'].minute < 5
all_sorted_series, yvals = ecdf.get_ecdf(df['freq'])
print "Plotting graph"
plt.plot(sorted_series, yvals, c="b", label="Netzfrequenz")
plt.legend(loc="lower right")
plt.title(u"Vergleich der Frequenzgänge")
#plt.xscale('log')
plt.xlabel('Frequenz [Hz]')
plt.ylabel(u'ECDF')
plt.savefig("images/ecdf.png", bbox_inches='tight')

