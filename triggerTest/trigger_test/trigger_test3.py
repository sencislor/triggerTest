'''
Created on Mar 20, 2017

@author: muly
'''
from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.trigger import coincidence_trigger
from obspy.signal.cross_correlation import templates_max_similarity
from pprint import pprint
import matplotlib.pyplot as plt
#from blaze.tests.test_utils import test_tmpfile

#st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ')
st = Stream()
st = read("2014080316.YN.mseed")
st = st.select(id='YN.QIJ.00.BHZ')
#st.filter('bandpass', freqmin=12, freqmax=20)
st.filter('bandpass', freqmin=10, freqmax=20)

'''
for tr in st:
    tr.plot()
'''
event_templates = {"QIJ": []}
t = UTCDateTime("2014-08-03T08:30:19.095000")
st_ = st.slice(t, t + 1)
event_templates["QIJ"] = [st_]

st2 = st.copy()
trace_ids = {'YN.QIJ.00.BHZ': 1}
similarity_thresholds = {"QIJ": 0.1}

'''
event_templates=[]
event_templates.append(st_)
trig = templates_max_similarity(st2, st[0].stats['starttime'], event_templates)
print(trig)
'''
trig = coincidence_trigger("classicstalta", 10, 1.5, st2, 1, sta=0.2, lta=5, 
                          trace_ids=trace_ids,
                          event_templates=event_templates,details=True,
                          delete_long_trigger=True, 
                          trigger_off_extension=2,
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

ax = plt.subplot(111)
plt.plot(st[0].data, 'k')

ymin, ymax = ax.get_ylim()
for t in trig:
    tt = (t['time']-st[0].stats['starttime'])/st[0].stats['delta']
    plt.vlines(tt, ymin, ymax, color='r', linewidth=2)
    #print((t['time']-st[0].stats['starttime'])/st[0].stats['delta'])

plt.show()

