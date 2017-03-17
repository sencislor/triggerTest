'''
Created on Mar 17, 2017

@author: muly
'''
from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.trigger import coincidence_trigger
from pprint import pprint

#st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ')
st = Stream()

files = ["BW.UH1..SHZ.D.2010.147.cut.slist.gz",
         "BW.UH2..SHZ.D.2010.147.cut.slist.gz",
         "BW.UH3..SHZ.D.2010.147.cut.slist.gz",
         "BW.UH3..SHN.D.2010.147.cut.slist.gz",
         "BW.UH3..SHE.D.2010.147.cut.slist.gz",
         "BW.UH4..SHZ.D.2010.147.cut.slist.gz"]
for filename in files:
    st += read(filename)

st.filter('bandpass', freqmin=10, freqmax=20)
'''
for tr in st:
    tr.plot()
'''
times = ["2010-05-27T16:24:33.095000", "2010-05-27T16:27:30.370000"]
event_templates = {"UH3": []}
for t in times:
    t = UTCDateTime(t)
    st_ = st.select(station="UH3").slice(t, t + 2.5)
    event_templates["UH3"].append(st_)
    
t = UTCDateTime("2010-05-27T16:27:30.574999")
st_ = st.select(station="UH1").slice(t, t + 2.5)
event_templates["UH1"] = [st_]

st2 = st.copy()
trace_ids = {"BW.UH1..SHZ": 1,
             "BW.UH2..SHZ": 1,
             "BW.UH3..SHZ": 1,
             "BW.UH4..SHZ": 1}
similarity_thresholds = {"UH1": 0.8, "UH3": 0.7}
trig = coincidence_trigger("classicstalta", 5, 1, st2, 4, sta=0.5,
                          lta=10, trace_ids=trace_ids,
                          event_templates=event_templates,
                          similarity_threshold=similarity_thresholds)

pprint(trig)


