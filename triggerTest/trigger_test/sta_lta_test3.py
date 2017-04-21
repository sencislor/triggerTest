from obspy import read
from obspy import UTCDateTime

from eqcorrscan.utils.trigger import TriggerParameters, network_trigger

'''
st = read("https://examples.obspy.org/" +
           "example_local_earthquake_3stations.mseed")
'''
st = read("2014080316.YN.mseed").select(network='YN',channel='BHZ')
parameters = []
for tr in st:
    parameters.append(TriggerParameters({'station': tr.stats.station,
                                          'channel': tr.stats.channel,
                                          'sta_len': 1,
                                          'lta_len': 10.0,
                                          'thr_on': 5.0,
                                          'thr_off': 3.0,
                                          'lowcut': 2.0,
                                          'highcut': 5.0}))
triggers = network_trigger(st=st, parameters=parameters,
                            thr_coincidence_sum=3, moveout=20,
                            max_trigger_length=60, despike=False)
evt_num =0 
for i in triggers:
    #print(u'duration: ', i[u'duration'])
    #print(u'coincidence_sum: ', i[u'coincidence_sum'])
    print(u'stations: ', i[u'stations'])
    #print(u'trace_ids: ', i[u'trace_ids'])
    #print(u'time: ', UTCDateTime(i[u'time']).strftime('%Y%m%d%H%M%S.%f'))   
    #print('-----------------------------------------------')
    print(UTCDateTime(i[u'time']).strftime('%Y%m%d%H%M%S.%f'),' ',
           i[u'duration'], ' ', i[u'coincidence_sum'])
    evt_num += 1
    
print(evt_num)
    
    
    