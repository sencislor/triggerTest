import matplotlib.pylab as plt
import numpy as np
from obspy import read
from obspy.signal.trigger import coincidenceTrigger



sta = 1
lta = 6
#cft = classicSTALTA(tr.data, int(sta * tr.stats.sampling_rate), int(lta * tr.stats.sampling_rate))
thr_on = 3.5
thr_off = 0.5
st = read('2014080316.YN.mseed')
st = st.select(network='YN', component="Z")
ids = []
for tr in st:
    ids.append(tr.id)
    
st.filter('bandpass', freqmin=10, freqmax=20)

res = coincidenceTrigger('recstalta', thr_on, thr_off, st, 4, sta=sta, lta=lta, trace_ids=ids)

count = 0
for ev in res:
    print(ev['coincidence_sum'])
    print(ev['stations'])
    print(ev['time'])
    print('---------------------------')
    count += 1
    
print(count)


