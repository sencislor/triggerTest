from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.trigger import coincidence_trigger
from obspy.signal.cross_correlation import templates_max_similarity
from pprint import pprint
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz
from eqcorrscan.core.template_gen import multi_template_gen
from obspy.core.event import read_events

catalog = read_events('ludian.xml')
for e in catalog:
    picks = e.picks
    for p in picks:
        print(p)

ynst = read("../seisdata/2014080316.YN.mseed").merge(fill_value=0)
st = ynst.select(station='QIJ')
st += ynst.select(station='DOC')
st += ynst.select(station='XUW')
print(st)
# st.plot()
templates = multi_template_gen(catalog, st, 2, plot=True)

for t in templates:
   # print(t)

    for tr in t:
        #print(tr.stats.network)
        #print(tr.stats.station)
        #print(tr.stats.channel)
        if tr.stats.channel == 'BZ':
            tr.stats.channel = 'BHZ'
        if tr.stats.channel == 'BE':
            tr.stats.channel = 'BHE'
        if tr.stats.channel == 'BN':
            tr.stats.channel = 'BHN'

        #print(tr)
    t.write('template.ms', format="MSEED")

#---------------------------------------------------------------------


