
from obspy.core import UTCDateTime
from obspy.core import inventory


#function to make date time
def make_datetime(a,b):
    a = a.split('/')
    return a[2]+'-'+a[1]+'-'+a[0]+' '+b


# path to ANU text file with station metadata
ANU_meta = '/media/obsuser/GA-ANU_TRAN/instr.coord'


with open(ANU_meta, 'r') as f:
    data=f.readlines()

station_list = []

for i, line in enumerate(data):
    fields = line.split(' ')
    surv_name = fields[9]

    print surv_name, fields[1]

    start_Date = UTCDateTime(make_datetime(fields[5], fields[6]))
    end_Date = UTCDateTime(make_datetime(fields[7], fields[8]))

    #create inventory for station
    Z_channel = inventory.Channel(code='BHZ', location_code='', depth=0, azimuth=270, dip=0, sample_rate=50,
                                  clock_drift_in_seconds_per_sample=0, latitude=fields[2], longitude=fields[3],
                                  elevation=fields[4])
    N_channel = inventory.Channel(code='BHN', location_code='', depth=0, azimuth=270, dip=0, sample_rate=50,
                                  clock_drift_in_seconds_per_sample=0, latitude=fields[2], longitude=fields[3],
                                  elevation=fields[4])
    E_channel = inventory.Channel(code='BHE', location_code='', depth=0, azimuth=270, dip=0, sample_rate=50,
                                  clock_drift_in_seconds_per_sample=0, latitude=fields[2], longitude=fields[3],
                                  elevation=fields[4])
    channels = [Z_channel, N_channel, E_channel]
    site = inventory.Site(name=fields[1], description=fields[10])
    station = inventory.Station(code=fields[1], creation_date=start_Date, termination_date=end_Date, latitude=fields[2],
                                longitude=fields[3], elevation=fields[4], vault='Transportable Array',
                                channels=channels, site=site)

    station_list.append(station)

    if i == len(data) - 1:
        network = inventory.Network(code=surv_name, alternate_code=fields[0], start_date=start_Date,
                                    stations=station_list)

        inv = inventory.Inventory(networks=[network], source='Geoscience Australia')

        print inv

        inv.write(path_or_file_object='/media/obsuser/seismic_data_1/_ANU/' + surv_name + '.xml', format='STATIONXML')

        break


    #compare the current iterated survey name to the next one in the text file
    if not surv_name == data[i+1].split(' ')[9]:
        # next line will be a new survey

        network = inventory.Network(code=surv_name, alternate_code=fields[0], start_date=start_Date, stations=station_list)

        inv = inventory.Inventory(networks=[network], source='Geoscience Australia')

        print inv

        inv.write(path_or_file_object='/media/obsuser/seismic_data_1/_ANU/' + surv_name + '.xml', format='STATIONXML')

        station_list=[]
        continue



