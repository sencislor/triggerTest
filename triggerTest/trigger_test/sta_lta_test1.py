import matplotlib.pylab as plt
import numpy as np
from obspy.signal.trigger import triggerOnset
import threading

from obspy import read
from obspy.signal.trigger import classicSTALTA#, plotTrigger

def plot_trigger(tr, cft, thr1, thr2):
    df, npts = tr.stats.sampling_rate, tr.stats.npts
    t = np.arange(npts,dtype='float32')/df
    fig = plt.figure(1)
    #fig = plt.figure(1, figsize=(8, 4))
    fig.clf()
    ax = fig.add_subplot(211)
    ax.plot(t, tr.data, 'black')
    ax2 = fig.add_subplot(212,sharex=ax)
    ax2.plot(t, cft, 'black')
    onof = np.array(triggerOnset(cft, thr1, thr2))
    print(onof)
    i,j = ax.get_ylim()
    try:
        ax.vlines(onof[:,0]/df, i, j, color='red', lw = 2)
        ax.vlines(onof[:,1]/df, i, j, color='blue', lw = 2)
    except IndexError:
        pass
    ax2.axhline(thr1, color='red', lw = 1, ls = '--')
    ax2.axhline(thr2, color='blue', lw = 1, ls = '--')
    fig.canvas.draw()
    plt.show()

def plot_threaded(tr, cft, thr1, thr2):
    thread = threading.Thread(target=plot_trigger, args=(tr, cft, thr1, thr2))
    thread.start()
    
#st = read('20140803.YN.QKT.mseed')
#tr = st.select(component="Z")[0]
st = read('2014080316.YN.mseed')
tr = st.select(id="YN.QIJ.00.BHZ")[0]
tr.filter("bandpass", freqmin=8, freqmax=20)
sta = 1
lta = 5
cft = classicSTALTA(tr.data, int(sta * tr.stats.sampling_rate), int(lta * tr.stats.sampling_rate))
thr_on = 3.5
thr_off = 0.5

plot_trigger(tr, cft, thr_on, thr_off)
