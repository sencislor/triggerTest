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
from obspy.signal.invsim import corn_freq_2_paz

paz = {'sensitivity': 1258650000.0,
       'poles': [-0.074+0.074j, -0.074-0.074j, -222+222j, -222-222j],
       'gain': 98570.0,
       'zeros': [0j, 0j]}
paz_1hz = corn_freq_2_paz(1.0, damp=0.707)  # 1Hz instrument
paz_1hz['sensitivity'] = 1.0

catalog = read_events('ludian.xml')
for e in catalog:
    picks = e.picks
    for p in picks:
        print(p)

ynst = read("2014080316.YN.mseed").sort(['starttime']).trim()

st = ynst.select(station='ZAT')
# st += ynst.select(station='QIJ')
# st += ynst.select(station='PGE')
# st += ynst.select(station='DOC')
# st += ynst.select(station='XUW')

st.simulate(paz_remove=paz, paz_simulate=paz_1hz)
st.detrend()
# st.filter('bandpass', freqmin=20, freqmax=30,corners=4)
st = pre_processing.shortproc(st, lowcut=2, highcut=9, filt_order=18, samp_rate=100,
                            starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)

st = Stream(st)
templates = multi_template_gen(catalog, st, 5.19, plot=True)

#t = UTCDateTime("2014-08-03T08:30:19.095000")
#st = st.slice(t-10, t+36000)

#st.plot()

for t in templates:
    print(t)
    t.write('template.ms', format="MSEED")
    # for tr in t:
    #     #print(tr.stats.network)
    #     #print(tr.stats.station)
    #     #print(tr.stats.channel)
    #     if tr.stats.channel == 'BZ':
    #         tr.stats.channel = 'BHZ'
    #     if tr.stats.channel == 'BE':
    #         tr.stats.channel = 'BHE'
    #     if tr.stats.channel == 'BN':
    #         tr.stats.channel = 'BHN'
    #     print(tr)
#read('template.ms').plot()


