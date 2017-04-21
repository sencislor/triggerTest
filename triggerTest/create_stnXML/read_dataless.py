from obspy.core import UTCDateTime
from obspy.core import inventory
from obspy.io.xseed.parser import Parser

sp = Parser('YN.dataless')
xsd = sp.get_xseed()
print(xsd)

#print(sp.get_inventory())["channels"]
#print(sp.get_inventory()["stations"])


#print(sp.getXSEED())

