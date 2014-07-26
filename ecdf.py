# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import freqanalysis.ecdf as ecdf
import freqanalysis.datatools as datatool
from scipy.stats import ks_2samp



datasetfile = "datasets/20140723-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)
print "Calculating ECDF of all values"
all_series, yvals = ecdf.get_ecdf(df['freq'])
print "Plotting graph"
ecdf.plot_ecdf_curve(all_series, yvals, color="b", label="Alle Werte")

df['minute'] = df.time.apply(lambda x: x.minute)

hour_df = df[(df.minute >= 58) | (df.minute <= 3)]
hour_series, yvals = ecdf.get_ecdf(hour_df['freq'])
ecdf.plot_ecdf_curve(hour_series, yvals, color="r",
    label="Stundenwechsel")

not_hour_df = df[(df.minute < 58 ) & (df.minute > 3)]
not_hour_series, yvals = ecdf.get_ecdf(not_hour_df['freq'])
ecdf.plot_ecdf_curve(not_hour_series, yvals, color="y", linestyle="-",
    label="unter der Stunde")
print "Null hypothesis: the two samples are drawn from the same continuous distribution."

D, p_value = ks_2samp(all_series, hour_series)
if p_value < 0.01:
  print "Rejecting null hypothesis - the two distributions differ significantly. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 abgelehnt (alpha=0.01)" % p_value
else:
  print "Accepting null hypothesis - the two distributions are the same. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 abgelehnt (alpha=0.01)" % p_value

plt.title(u"Netzfrequenz, %s" % ks_comment)
plt.savefig("images/ecdf.png", bbox_inches='tight')
