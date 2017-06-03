"""
Created on Mar 20, 2017
@author: muly
"""
from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.trigger import coincidence_trigger
from obspy.signal.cross_correlation import templates_max_similarity
from pprint import pprint
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz
# from blaze.tests.test_utils import test_tmpfile

paz2 = {'sensitivity': 1258650000.0,
       'poles': [-0.074+0.074j, -0.074-0.074j, -222+222j, -222-222j],
       'gain': 98570.0,
       'zeros': [0j, 0j]}

paz_1hz = corn_freq_2_paz(1.0, damp=0.707)  # 1Hz instrument
paz_1hz['sensitivity'] = 1.0

t = UTCDateTime("2014-08-03T08:30:19.095000")

# st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ')
st = read("../seisdata/2014080316.YN.mseed").select(id='YN.QIJ.00.BHZ')
st = st.slice(t-10, t + 3600)
st.simulate(paz_remove=paz2, paz_simulate=paz_1hz)
org_st = st.copy()
fil_st = st.copy()
# st = read('20140803.YN.QIJ.mseed').select(network='YN',channel='BHZ')

# st.filter('bandpass', freqmin=12, freqmax=20)
st.filter('bandpass', freqmin=20, freqmax=30)
# st.filter("highpass", freq=20)
fil_st.filter('bandpass', freqmin=1, freqmax=10)

'''
for tr in st:
    tr.plot()
'''
event_templates = {"QIJ": []}
st_ = st.slice(t, t + 2)
event_templates["QIJ"] = [st_]

trace_ids = {'YN.QIJ.00.BHZ': 1}
similarity_thresholds = {"QIJ": 0.6}

'''
event_templates=[]
event_templates.append(st_)
trig = templates_max_similarity(st2, st[0].stats['starttime'], event_templates)
print(trig)
'''
trig = coincidence_trigger("classicstalta", 4, 0.5, st, 1, sta=0.4, lta=5,
                          trace_ids=trace_ids,
                          event_templates=event_templates,
                          details=True,
                          delete_long_trigger=True,
                          trigger_off_extension=5,
                          similarity_threshold=similarity_thresholds)
'''
trig = coincidence_trigger("classicstalta", 10, 1, st2, 1, sta=0.2, lta=5, 
                          trace_ids=trace_ids,
                          event_templates=event_templates,details=True,
                          delete_long_trigger=True, 
                          trigger_off_extension=5,
                          similarity_threshold=similarity_thresholds)
'''
#pprint(trig)

f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=False)
ax1.plot(org_st[0].data, 'k')
ax2.plot(st[0].data, 'k')
ax3.plot(fil_st[0].data, 'k')
y1min, y1max = ax1.get_ylim()
y2min, y2max = ax2.get_ylim()
y3min, y3max = ax3.get_ylim()
evt_sum = 0

for t in trig:
    tt = (t['time']-st[0].stats['starttime'])/st[0].stats['delta']
    ax1.vlines(tt, y1min, y1max, color='r', linewidth=2)
    ax2.vlines(tt, y2min, y2max, color='r', linewidth=2)
    ax3.vlines(tt, y3min, y3max, color='r', linewidth=2)
    evt_sum += 1
    # print((t['time']-st[0].stats['starttime'])/st[0].stats['delta'])
    print(t['time'])
print(evt_sum)
plt.show()