import matplotlib.pyplot as plt
import freqanalysis.datatools as datatool

def draw_target_cross(ax, time, freq, labeltext):
  time_line = (datatool.unix2time(time), datatool.unix2time(time))
  ax.plot(time_line, ax.get_ylim(), 'r--', label=labeltext)
  freq_line = (freq, freq)
  ax.plot(ax.get_xlim(), freq_line, 'r--')
  ax.plot((datatool.unix2time(time)), (freq), 'ro')

