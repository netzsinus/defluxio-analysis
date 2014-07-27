import numpy as np
import pandas as pd

def filter_absolute_positive_deviation(df, mHz_threshold):
  hz_threshold = mHz_threshold / 1000.0
  return df[(df.freq >= (50.0 + hz_threshold))]


def filter_absolute_negative_deviation(df, mHz_threshold):
  hz_threshold = mHz_threshold / 1000.0
  return df[(df.freq <= (50.0 - hz_threshold))]


