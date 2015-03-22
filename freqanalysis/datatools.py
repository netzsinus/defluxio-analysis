import numpy as np
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

def load_data_as_dataframe(filename):
  datafile = open(filename)
  datafile.readline() # skip the header
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

# Helper: convert seconds of day to HH:MM formatted string
def seconds_to_timeofday(timestamp):
  localized = pytz.utc.localize(dt.datetime.fromtimestamp(timestamp))
  return localized.strftime('%H:%M')

def seconds_to_date(timestamp):
  localized = pytz.utc.localize(dt.datetime.fromtimestamp(timestamp))
  return localized.strftime('%d.%m.%Y')

