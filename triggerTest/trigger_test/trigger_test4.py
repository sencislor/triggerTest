from obspy import read
from obspy import Stream, read
from obspy.core import UTCDateTime

st = read("../seisdata/2014080316.YN.mseed")
tr = st.select(id='YN.QIJ.00.BHZ')
st.filter('bandpass', freqmin=10, freqmax=20)

event_templates = []
t = UTCDateTime("2014-08-03T08:30:19.029")
st_ = st.select(station="QIJ").slice(t, t + 2.5)
event_templates.apent(st_)