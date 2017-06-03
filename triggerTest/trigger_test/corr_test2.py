from eqcorrscan.core import match_filter
from eqcorrscan.utils import pre_processing
from obspy import read
from obspy.core import UTCDateTime

t = UTCDateTime("2014-08-03T08:30:19.095000")

st = read("../seisdata/2014080316.YN.mseed").merge(fill_value=0).select(id='YN.QIJ.00.BH?')
st = st.slice(t-10, t + 3600)

st = pre_processing.dayproc(st, lowcut=2, highcut=10, filt_order=4,
                            samp_rate=100,
                            starttime=st[0].stats.starttime.date)

# Read in the templates
templates = []
template_names = ['template.ms']
for template_file in template_names:
     templates.append(read(template_file))

detections = match_filter.match_filter(template_names=template_names,
                                       template_list=templates, st=st,
                                       threshold=8, threshold_type='MAD',
                                       trig_int=1, plotvar=False,
                                       cores=1)
