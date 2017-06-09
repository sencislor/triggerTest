from eqcorrscan.core import match_filter
from eqcorrscan.utils import pre_processing
from obspy import read, Stream
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz
from eqcorrscan.utils.plotting import multi_trace_plot
from eqcorrscan.utils.plotting import detection_multiplot

paz = {'sensitivity': 1258650000.0,
       'poles': [-0.074+0.074j, -0.074-0.074j, -222+222j, -222-222j],
       'gain': 98570.0,
       'zeros': [0j, 0j]}
paz_1hz = corn_freq_2_paz(1.0, damp=0.707)  # 1Hz instrument
paz_1hz['sensitivity'] = 1.0

t = UTCDateTime("2014-08-03T08:30:19.095000")

ynst = read("2014080316.YN.mseed")
st = ynst.select(station='ZAT').sort(['starttime']).trim()
# st += ynst.select(station='QIJ')
# st += ynst.select(station='PGE')
# st += ynst.select(station='DOC')
# st += ynst.select(station='XUW')
#st = read("20140803.YN.QIJ.mseed").merge(fill_value=0).select(id='YN.QIJ.00.BH?')
st = st.slice(t-30, t + 1800)

st.simulate(paz_remove=paz, paz_simulate=paz_1hz)
st.detrend()

# st.filter('bandpass', freqmin=20, freqmax=30)
# st.filter('bandpass', freqmin=2, freqmax=10,corners=100)
st = pre_processing.shortproc(st, lowcut=2, highcut=9, filt_order=18,
                            samp_rate=100,
                            starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)
st = Stream(st)
# st.plot()
# Read in the templates
templates = []
template_names = ['template.ms']
for template_file in template_names:
     templates.append(read(template_file))

detections = match_filter.match_filter(template_names=template_names,
                                       template_list=templates, st=st,
                                       threshold=5.5, threshold_type='MAD',
                                       trig_int=1, plotvar=True,
                                       cores=6)

for detection in detections:
     #detection.write('detections.csv', append=True)
     detection.write('detections.csv')

# plot
# multi_trace_plot(st, corr=True, stack='linstack', size=(7, 12), show=True, title=None)

times=[]
for dc in detections:
    for pick in dc.event.picks:
        times.append(pick.time)
template = read('template.ms')
template.plot()
detection_multiplot(st,template,times,streamcolour='k',templatecolour='r')

# f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=False)
# ax1.plot(st.select(id='YN.ZAT.00.BZ')[0].data, 'k')
# y1min, y1max = ax1.get_ylim()
# ax2.plot(st.select(id='YN.ZAT.00.BE')[0].data, 'k')
# y2min, y2max = ax2.get_ylim()
# ax3.plot(st.select(id='YN.ZAT.00.BN')[0].data, 'k')
# y3min, y3max = ax3.get_ylim()
#
# for detection in detections:
#     t = detection.detect_time
#     tt = (t- st[0].stats['starttime']) / st[0].stats['delta']
#     ax1.vlines(tt, y1min, y1max, color='r', linewidth=2)
#     ax2.vlines(tt, y2min, y2max, color='r', linewidth=2)
#     ax3.vlines(tt, y3min, y3max, color='r', linewidth=2)
#
# plt.show()

# print(st[0].stats.channel)
# print(len(st[0].data))
# print(st[0].stats.starttime)
# print(st[0].stats.endtime)
# print(st[1].stats.channel)
# print(len(st[1].data))
# print(st[1].stats.starttime)
# print(st[1].stats.endtime)
# print(st[2].stats.channel)
# print(len(st[2].data))
# print(st[2].stats.starttime)
# print(st[2].stats.endtime)
# var = st[0].data * st[1].data *st[2].data
# plt.plot(var)
# plt.show()

# var = st.select(id='YN.ZAT.00.BZ')[0].data * st.select(id='YN.ZAT.00.BE')[0].data
