# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import numpy as np
import datetime as dt

def load_data(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  return time, data[:,1]

#datasetfile = "datasets/20140728-export.txt"
datasetfile = "datasets/20140815-export.txt"
diotime, diofreq = load_data(datasetfile)
plt.close('all')
(mu, sigma) = norm.fit(diofreq)
# use 3sigma rule for over/underfreq detection
upper_freq_limit = mu+3*sigma
lower_freq_limit = mu-3*sigma


f, axarr = plt.subplots(2)
plt.title("Netzfrequenz")

axarr[0].set_title("Verlauf der Netzfrequenz")
axarr[0].set_xlabel("Zeit")
axarr[0].set_ylabel("Frequenz [Hz]")
axarr[0].plot(diotime, diofreq, 'b', label="Defluxio")
#plt.legend()
axarr[0].plot(axarr[0].get_xlim(), (lower_freq_limit, lower_freq_limit), 'r-')
axarr[0].plot(axarr[0].get_xlim(), (upper_freq_limit, upper_freq_limit), 'r-')

# the histogram of the data
n, bins, patches = axarr[1].hist(diofreq, 100, normed=1, facecolor='green', alpha=0.75)
# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = axarr[1].plot(bins, y, 'r--', linewidth=1)
axarr[1].set_xlabel('Frequenz [Hz]')
axarr[1].set_ylabel(u'Häufigkeit')
axarr[1].set_title(r'$\mathrm{Histogram\ der\ Frequenz:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))

# add 3sigma lines to the plots
axarr[1].plot((lower_freq_limit, lower_freq_limit),
    axarr[1].get_ylim(), 'r-')
axarr[1].plot((upper_freq_limit, upper_freq_limit),
    axarr[1].get_ylim(), 'r-')
axarr[1].grid(True)


#print "Mittelwert Netzfrequenz:", np.mean(diofreq)
#print "Median Netzfrequenz:", np.median(diofreq)
#print "Maximalwert Netzfrequenz:", np.max(diofreq)
#print "Minimalwert Netzfrequenz:", np.min(diofreq)

#plt.figure()
#lastweek_time, lastweek_freq = load_data("lastweek-frequenz.txt")
#plt.title("Netzfrequenz: Letzte Woche")
#plt.xlabel("Zeit")
#plt.ylabel("Frequenz [Hz]")
#plt.plot(lastweek_time, lastweek_freq, 'b', label="Letzte Woche (ITWM)")
#plt.legend()

plt.tight_layout()
plt.savefig("images/frequenzverlauf.png", bbox_inches='tight')

