# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib as mpl
import numpy as np
import datetime as dt

def load_data(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  return time, data[:,1]

f, ax = plt.subplots()
lower_freq_limit = 49.95
upper_freq_limit = 50.05
time, freq = load_data("datasets/20150320-sonnenfinsternis.txt")
ax.set_xlabel("Zeit")
ax.set_ylabel("Frequenz [Hz]")
ax.set_ylim((lower_freq_limit, upper_freq_limit))
ax.plot(time, freq, 'b', label="Netzfrequenz")
ax.plot(ax.get_xlim(), (50.0, 50.0), 'r-', label="Sollwert")
ax.legend()
hfmt = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hfmt)
y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax.yaxis.set_major_formatter(y_formatter)
ax.grid(True)

# http://docs.scipy.org/doc/numpy/reference/generated/numpy.ediff1d.html#numpy.ediff1d

#plt.figure()
#lastweek_time, lastweek_freq = load_data("lastweek-frequenz.txt")
#plt.title("Netzfrequenz: Letzte Woche")
#plt.xlabel("Zeit")
#plt.ylabel("Frequenz [Hz]")
#plt.plot(lastweek_time, lastweek_freq, 'b', label="Letzte Woche (ITWM)")
#plt.legend()
f.suptitle("Sonnenfinsternis am 20.03.2015")
f.autofmt_xdate()
plt.savefig("images/sonnenfinsternis.png")#, bbox_inches='tight')
