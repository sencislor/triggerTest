from obspy import read
from obspy.xseed import Parser
from obspy.signal.spectral_estimation import PPSD

#st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ',station='QIJ')
st = read("2014080316.YN.mseed")
tr = st.select(id='YN.QIJ.00.BHZ')[0]
tr = tr.filter('bandpass', freqmin=1, freqmax=5)
tr.plot()

'''
parser = Parser("YN.dataless")
paz = parser.getPAZ(tr.id)
ppsd = PPSD(tr.stats, paz)
ppsd.add(tr)
ppsd.plot()
'''

