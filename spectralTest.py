'''
Created on Apr 18, 2017

@author: muly
'''
from obspy.core import read
from obspy.io.xseed.parser import Parser
from obspy.imaging.cm import pqlx
#from obspy.signal import PPSD
from single.spectral import PPSD

ynpar = Parser('YN.dataless')

#st = read('20140901.YN.XIM.mseed')
#tr = st.select(id='YN.XIM.00.SHZ')[0]

#st = read('20140803.YN.CAY.mseed')
#tr = st.select(id='YN.CAY.00.BHZ')[0]
st = read('20140807.YN.FUN.mseed')
tr = st.select(id='YN.FUN.00.BHZ')[1]

paz =ynpar.get_paz("%(network)s.%(station)s.%(location)s.%(channel)s" % tr.stats)
'''
paz = {'sensitivity': 1258650000.0, 
       'poles': [-0.074+0.074j, -0.074-0.074j, -222+222j, -222-222j], 
       'gain': 98570.0, 
       'zeros': [0j, 0j]}
'''
#paz = {'sensitivity': 1258650000.0}

#datalen = tr.stats.endtime - tr.stats.starttime


'''
When using `special_handling="ringlaser"` the applied processing
steps are changed. Differentiation of data (converting velocity
to acceleration data) will be omitted and a flat instrument
response is assumed, leaving away response removal and only
dividing by `metadata['sensitivity']` specified in the provided
`metadata` dictionary (other keys do not have to be present
then). For scaling factors that are usually multiplied to the
data remember to use the inverse as `metadata['sensitivity']`.

'''
#ppsd = PPSD(tr.stats, paz, special_handling="ringlaser", ppsd_length=3600.0/2)
ppsd = PPSD(tr.stats, paz, special_handling="convert", ppsd_length=3600.0/2)
#ppsd = PPSD(tr.stats, paz, ppsd_length=3600.0/2)
ppsd.add(st)
ppsd.save_npz("%(network)s.%(station)s.%(location)s.%(channel)s.psd" % tr.stats)
#print(ppsd.get_mode())
#print(ppsd.get_mean())
#ppsd.plot_coverage()
ppsd.load_npz("%(network)s.%(station)s.%(location)s.%(channel)s.psd.npz" % tr.stats)
ppsd.plot(show_mean=False, 
          show_coverage=True, 
          show_histogram=True, 
          show_percentiles=False, 
          show_mode=True,
          mode_linewidth=2,
          mode_color='red',
          percentiles=[0, 25, 50, 75, 100], 
          cumulative_number_of_colors=60, 
          xaxis_frequency=True, 
          period_lim=(0.1, 100))
#ppsd.plot(cmap=pqlx)
