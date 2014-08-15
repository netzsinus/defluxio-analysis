# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import ks_2samp
from scipy.stats.mstats import normaltest
import freqanalysis.datatools as datatool
import freqanalysis.normdist as nd



datasetfile = "datasets/20140815-export.txt"
print "loading ", datasetfile
df = datatool.load_data_as_dataframe(datasetfile)
df['minute'] = df.time.apply(lambda x: x.minute)
hour_df = df[(df.minute >= 58) | (df.minute <= 5)]
not_hour_df = df[(df.minute < 58) & (df.minute > 5)]

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
# pandas/matplotlib incompatibility: http://stackoverflow.com/a/22764377
nd.plot_fit(df['freq'].values, ax1, "Alle\ Werte")
nd.plot_fit(hour_df['freq'].values, ax2, "Nur\ Stundenwechsel")
nd.plot_fit(not_hour_df['freq'].values, ax3, "Kein\ Stundenwechsel")

f.savefig("images/normdistrib.png", bbox_inches='tight')

print
print "Executing KS-Test: is the data normally distributed?"
mu, std = norm.fit(df['freq'])
refdist = np.random.normal(mu, std, 100000)
D, p_value = ks_2samp(df['freq'].values, refdist)
if p_value < 0.01:
  print "Rejecting null hypothesis - the two distributions differ significantly. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 rejected (alpha=0.01)" % p_value
else:
  print "Accepting null hypothesis - the two distributions are the same. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 accepted (alpha=0.01)" % p_value

#print
#print "Executing D'Agostino, 'An omnibus test of normality for moderate and large sample size', Biometrika, 58, 341-348"
#k2, p_value = normaltest(df['freq'])
#if p_value < 0.01:
#  print "Rejecting null hypothesis - the dataset is not normally distributed. p = %.4f" % p_value
#  omnibus_comment = "Omnibus: p=%.4f, H0 rejected (alpha=0.01)" % p_value
#else:
#  print "Accepting null hypothesis - the dataset is normally distributed. p = %.4f" % p_value
#  omnibus_comment = "Omnibus: p=%.4f, H0 accepted (alpha=0.01)" % p_value
#
