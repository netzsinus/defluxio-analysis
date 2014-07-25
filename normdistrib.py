# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import ks_2samp
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

print "Executing KS-Test: is the data normally distributed?"
mu, std = norm.fit(df['freq'])
refdist = np.random.normal(mu, std, 10000)
D, p_value = ks_2samp(df['freq'].values, refdist)

if p_value < 0.01:
  print "Rejecting null hypothesis - the two distributions differ significantly. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 rejected" % p_value
else:
  print "Accepting null hypothesis - the two distributions are the same. p = %.4f" % p_value
  ks_comment = "KS: p=%.4f, H0 accepted" % p_value


