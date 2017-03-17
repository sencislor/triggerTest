from obspy.core.inventory.inventory import read_inventory
#from obspy import read_inventory

inv = read_inventory('yn_station.xml', format='stationxml')
#inv.plot()
nets = inv.get_contents()['networks']
print(nets)
n = inv.select('YN')
#print(n)
for net in inv:
    #print(net.get_contents())
    pass