# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

def load_data(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  return time, data[:,1]

rhrk_time, rhrk_freq = load_data("datasets/rhrk-vergleichsfrequenz.txt")
defluxio_time, defluxio_freq = load_data("datasets/defluxio-vergleichsfrequenz.txt")
plt.title("Netzfrequenz: Janitza 604E vs. Defluxio")
plt.xlabel("Zeit")
plt.ylabel("Frequenz [Hz]")
plt.plot(rhrk_time, rhrk_freq, 'r', label="Janitza")
plt.plot(defluxio_time, defluxio_freq, 'b', label="Defluxio")
plt.legend()

print "Mittelwert Janitza:", np.mean(rhrk_freq)
print "Mittelwert Defluxio:", np.mean(defluxio_freq)

#plt.figure()
#lastweek_time, lastweek_freq = load_data("lastweek-frequenz.txt")
#plt.title("Netzfrequenz: Letzte Woche")
#plt.xlabel("Zeit")
#plt.ylabel("Frequenz [Hz]")
#plt.plot(lastweek_time, lastweek_freq, 'b', label="Letzte Woche (ITWM)")
#plt.legend()



plt.show()
