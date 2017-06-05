from eqcorrscan.core import match_filter
from eqcorrscan.utils import pre_processing
from obspy import read
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt

t = UTCDateTime("2014-08-03T08:30:19.095000")

ynst = read("2014080316.YN.mseed").sort().merge()
st = ynst.select(station='ZAT')
st += ynst.select(station='QIJ')
st += ynst.select(station='PGE')
st += ynst.select(station='DOC')
st += ynst.select(station='XUW')
#st = read("20140803.YN.QIJ.mseed").merge(fill_value=0).select(id='YN.QIJ.00.BH?')
st = st.slice(t-10, t + 1800)

st = pre_processing.shortproc(st, lowcut=2, highcut=10, filt_order=4,
                            samp_rate=100,
                            starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)

# Read in the templates
templates = []
template_names = ['template.ms']
for template_file in template_names:
     templates.append(read(template_file))

detections = match_filter.match_filter(template_names=template_names,
                                       template_list=templates, st=st,
                                       threshold=9, threshold_type='MAD',
                                       trig_int=1, plotvar=True,
                                       cores=1)

print(detections)
for detection in detections:
     detection.write('detections.csv', append=True)

f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=False)
ax1.plot(st.select(id='YN.ZAT.00.BZ')[0].data, 'k')
ax2.plot(st.select(id='YN.QIJ.00.BZ')[0].data, 'k')
ax3.plot(st.select(id='SC.PGE.00.BZ')[0].data, 'k')
y1min, y1max = ax1.get_ylim()
y2min, y2max = ax2.get_ylim()
y3min, y3max = ax3.get_ylim()

for detection in detections:
    t = detection.detect_time
    tt = (t- st[0].stats['starttime']) / st[0].stats['delta']
    ax1.vlines(tt, y1min, y1max, color='r', linewidth=2)
    ax2.vlines(tt, y2min, y2max, color='r', linewidth=2)
    ax3.vlines(tt, y3min, y3max, color='r', linewidth=2)

plt.show()