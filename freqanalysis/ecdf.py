import numpy as np
import matplotlib.pyplot as plt

def get_ecdf(series):
  sorted_series = np.sort(series)
  yvals = np.arange(len(sorted_series))/float(len(sorted_series))
  return sorted_series, yvals

def plot_ecdf_curve(sorted_series, yvals, color='b', label="ECDF",
    linestyle = '-'):
  plt.plot(sorted_series, yvals, c=color, label=label,
      linestyle=linestyle, linewidth = 2)
  plt.legend(loc="best")
  plt.xlabel('Frequenz [Hz]')
  plt.ylabel(u'ECDF')


