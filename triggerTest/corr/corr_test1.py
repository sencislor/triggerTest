from obspy import Stream, read
from obspy.core import UTCDateTime
from obspy.signal.trigger import coincidence_trigger
from obspy.signal.cross_correlation import templates_max_similarity
from pprint import pprint
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz
from eqcorrscan.core.template_gen import multi_template_gen
from obspy.core.event import read_events
from eqcorrscan.utils import pre_processing

catalog = read_events('ludian.xml')
for e in catalog:
    picks = e.picks
    for p in picks:
        print(p)

ynst = read("2014080316.YN.mseed").sort().merge()

st = ynst.select(station='ZAT')
st += ynst.select(station='QIJ')
st += ynst.select(station='PGE')
st += ynst.select(station='DOC')
st += ynst.select(station='XUW')

#st.filter('bandpass', freqmin=1, freqmax=10,corners=4)
st = pre_processing.shortproc(st, lowcut=2, highcut=10, filt_order=4, samp_rate=100,
                            starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)

templates = multi_template_gen(catalog, st, 5, plot=True)

#t = UTCDateTime("2014-08-03T08:30:19.095000")
#st = st.slice(t-10, t+36000)

#st.plot()

for t in templates:
    print(t)
    t.write('template.ms', format="MSEED")
    # for tr in t:
        #print(tr.stats.network)
        #print(tr.stats.station)
        #print(tr.stats.channel)
        # if tr.stats.channel == 'BZ':
        #     tr.stats.channel = 'BHZ'
        # if tr.stats.channel == 'BE':
        #     tr.stats.channel = 'BHE'
        # if tr.stats.channel == 'BN':
        #     tr.stats.channel = 'BHN'
        #print(tr)
#read('template.ms').plot()


