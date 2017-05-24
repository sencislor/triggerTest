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
# from blaze.tests.test_utils import test_tmpfile

# st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ')
st = read("2014080316.YN.mseed").select(id='YN.QIJ.00.BHZ')
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
t = UTCDateTime("2014-08-03T08:30:19.095000")
st_ = st.slice(t, t + 2)
event_templates["QIJ"] = [st_]

st2 = st.copy()
trace_ids = {'YN.QIJ.00.BHZ': 1}
similarity_thresholds = {"QIJ": 0.6}

'''
event_templates=[]
event_templates.append(st_)
trig = templates_max_similarity(st2, st[0].stats['starttime'], event_templates)
print(trig)
'''
st = st.slice(t-10, t + 3600)
org_st = org_st.slice(t-10, t + 3600)
fil_st = fil_st.slice(t-10, t + 3600)
trig = coincidence_trigger("classicstalta", 4, 0.5, st.slice(t-10, t + 3600), 1, sta=0.4, lta=5,
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
print(evt_sum)
plt.show()




