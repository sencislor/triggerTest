from obspy import UTCDateTime
from obspy.io.xseed import Parser
from obspy.core import inventory

p = Parser('YN.dataless')

networks = p.get_inventory()["networks"]
stations = p.get_inventory()['stations']
channels = p.get_inventory()["channels"]

i=0
for n1 in networks:
    i = i + 1
    for n2 in networks[i:]:
        if n2['network_code'] == n1['network_code']:
            networks.remove(n2)
     
#print(networks)
#print(stations)
#print(channels)

network_list = []
for net in networks:
    station_list = []
    network_code = net['network_code']
    network_name = net['network_name']
    for stn in stations:
        stn_net = stn['station_id'].split('.')[0]
        if stn_net == network_code:
            channel_list = []
            station_code = stn['station_name']
            if station_code == '':
                station_code = stn['station_id'].split('.')[1]
            station_id = stn['station_id']
            for cha in channels:
                channel_id = cha[u'channel_id']
                channel_info = channel_id.split('.') 
                net_name = channel_info[0]
                stn_name = channel_info[1]
                site_name = channel_info[2]
                chn_name = channel_info[3]
                if stn_name == station_code and net_name == network_code:
                    longitude  = cha[u'longitude'] 
                    latitude   = cha[u'latitude'] 
                    elevation  = cha[u'elevation_in_m'] 
                    depth      = cha[u'local_depth_in_m'] 
                    instrument = cha[u'instrument'] 
                    sampling   = cha[u'sampling_rate'] 
                    start_date = cha[u'start_date']
                    if start_date == '':
                        start_date = UTCDateTime(1970, 1, 1, 0, 0)
                    end_date = cha[u'end_date'] 
                    if end_date =='':
                        end_date = UTCDateTime(2999, 1, 1, 0, 0)

                    #create inventory for station
                    stan_channel = inventory.Channel(code=chn_name, location_code=site_name, depth=depth, azimuth=270, 
                                                    dip=0, sample_rate=sampling, clock_drift_in_seconds_per_sample=0, 
                                                    latitude=latitude, longitude=longitude, elevation=elevation)
                    
                    channel_list.append(stan_channel)
                    site = inventory.Site(name=site_name, description=instrument)
                    station = inventory.Station(code=station_code, creation_date=start_date, 
                                                termination_date=end_date, latitude=latitude,
                                                longitude=longitude, elevation=elevation, vault=station_id,
                                                channels=channel_list, site=site)
                
            station_list.append(station)
                
    network = inventory.Network(code=network_code, alternate_code=network_name, 
                                start_date=start_date, stations=station_list)
    network_list.append(network)
inv = inventory.Inventory(networks=network_list, source='YN.dataless')
    
#print inv
    
inv.write(path_or_file_object='yn_station' + '.xml', format='STATIONXML')

                    