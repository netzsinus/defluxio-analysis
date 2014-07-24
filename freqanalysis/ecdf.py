import numpy as np

def get_ecdf(series):
  sorted_series = np.sort(series)
  yvals = np.arange(len(sorted_series))/float(len(sorted_series))
  return sorted_series, yvals
