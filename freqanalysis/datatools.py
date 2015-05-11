import numpy as np
import scipy.signal as sig
import datetime as dt
import time as t
import pandas as pd
import pytz

def load_data_as_series(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
  data = np.loadtxt(datafile)
  time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  return pd.Series(data[:,1], time)

def unix2ts(unix):
  # see http://stackoverflow.com/a/7065242
  unaware = dt.datetime.utcfromtimestamp(unix)
  return pytz.utc.localize(unaware)
  #return dt.datetime.fromtimestamp(unix)
  #return unaware.replace(tzinfo=pytz.UTC)

def ts2time(timestamp):
  return timestamp.time()

def unix2time(unix):
  return ts2time(unix2ts(unix))

def addSavitzkyGolay(dataframe):
  dataframe['freq_sg'] = sig.savgol_filter(dataframe['freq'], 7, 2)
  return dataframe

def secs_per_day():
  return 24*60*60

def load_data_as_dataframe(filename):
  datafile = open(filename)
  data = np.loadtxt(datafile)
  #data[:,0] = pd.to_datetime(data[:,0])
  #time = [dt.datetime.fromtimestamp(ts) for ts in data[:,0]]
  retval = pd.DataFrame(data, columns = ['unix', 'freq'])
  retval['ts'] = pd.to_datetime(retval['unix'].astype(int), unit='s',
      utc=True)
  retval['freq'] = retval['freq'].astype(float)
  retval['date'] = [c.date() for c in retval['ts']]
  retval['time'] = [c.time() for c in retval['ts']]
  retval['hour'] = retval.time.apply(lambda x: x.hour)
  retval['minute'] = retval.time.apply(lambda y: y.minute)
  retval['weekday'] = retval.date.apply(lambda z: z.weekday())
  min_ts = np.min(retval['ts'])
  #retval['d_since_start'] = [np.timedelta64(c, 'D').astype(int) for c in retval['ts'] - min_ts]
  min_unix = np.min(retval['unix'])
  #TODO: Skalierung ist kaputt. Siehe debug-output.
  daystart_offset = min_unix % (60*60*24)
  retval['d_since_start'] = ((retval['unix'] - (min_unix -
    daystart_offset) ) / (60*60*24)).astype(int)
  retval['s_since_midnight'] = [ c % (60*60*24) for c in retval['unix'] ]
  return retval

# See UCTE Handbook Appendix 1, p. 20f: https://www.entsoe.eu/fileadmin/user_upload/_library/publications/entsoe/Operation_Handbook/Policy_1_Appendix%20_final.pdf
def calc_trumpet_curve(starttime, f0, f1, df2, dPa):
  idx = np.arange(0, 900)
  A = 1.2 * df2
  T = 900/(np.log(np.abs(A/0.020)))
  trumpetneg = []
  trumpetpos = []
  for t in idx:
    trumpetneg.append(f0+A*np.exp(-t/T))
    trumpetpos.append(f0-A*np.exp(-t/T))
  idx = idx + starttime
  ts = []
  for t in idx:
    ts.append(unix2time(t))
  return pd.DataFrame({
    'time': ts,
    'trumpneg': trumpetneg,
    'trumppos': trumpetpos,
    })

# Calculate the momentum (1st order derivative) of the frequency data
def resample_add_freq_momentum(dataset, network_load):
  # First: Resample the dataset.
  resampling_interval = 2
  dataset = dataset.set_index(pd.DatetimeIndex(dataset['ts']))
  dataset = dataset.resample("%ss" % resampling_interval)
  # http://docs.scipy.org/doc/numpy/reference/generated/numpy.ediff1d.html#numpy.ediff1d
  momentum = np.ediff1d(dataset.freq_sg, to_begin=np.array([0]))
  # Entso-E has published 19.5 GW/Hz. We resampled to
  # resampling_interval seconds -> need to correct to 60s data
  dataset['momentum'] = momentum * network_load / (resampling_interval/60.0)
  return dataset.dropna()

# Helper: convert seconds of day to HH:MM formatted string
def seconds_to_timeofday(timestamp):
  localized = pytz.utc.localize(dt.datetime.fromtimestamp(timestamp))
  return localized.strftime('%H:%M')

def seconds_to_date(timestamp):
  localized = pytz.utc.localize(dt.datetime.fromtimestamp(timestamp))
  return localized.strftime('%d.%m.%Y')

