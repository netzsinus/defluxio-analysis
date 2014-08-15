import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


def plot_fit(data, ax, prefix):
  # Fit a normal distribution to the data:
  mu, std = norm.fit(data)
  mindata = np.min(data)
  maxdata = np.max(data)
  # Plot the histogram.
  ax.hist(data, bins=100, normed=True, alpha=0.6, color='g')
  # Plot the PDF.
  x = np.linspace(mindata, maxdata, 100)
  p = norm.pdf(x, mu, std)
  ax.plot(x, p, 'k', linewidth=2)
  title = r"$\mathrm{%s:}\ \mu = %.4f, \sigma = %.4f, n = %d$" % (prefix, mu, std, len(data))
  ax.set_title(title)
