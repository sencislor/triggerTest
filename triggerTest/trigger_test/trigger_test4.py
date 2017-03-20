from obspy import read
from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.cross_correlation import templates_max_similarity
import matplotlib.pyplot as plt

st = read("../seisdata/2014080316.YN.mseed")
st = st.select(id='YN.QIJ.00.BHZ')
st.filter('bandpass', freqmin=10, freqmax=20)

event_templates = []
t = UTCDateTime("2014-08-03T08:30:19.129")
st_ = st.select(station="QIJ").slice(t, t + 30)
event_templates.append(st_)

start_time = st[0].stats['starttime']
end_time   = st[0].stats['endtime']
move_time = start_time

ax = plt.subplot(111)
plt.plot(st[0].data, 'k')
while(move_time < end_time):
	cv = templates_max_similarity(st, move_time, event_templates)
	if cv >= 0.3:
		print(cv)
		print(move_time)
	
		tp = (move_time - start_time) * 100
		ymin, ymax = ax.get_ylim()
		plt.vlines(tp, ymin, ymax, color='r', linewidth=2)
		
		step = 30
	else:
		step = 0.1
		
	move_time = move_time + step
	
plt.show()

