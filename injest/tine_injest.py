# read archive channels from tine and prepare .json files to be later injested by the db
import PyTine as pt
from datetime import datetime
import json
import sys
import time

def get_device_list(property):
    d=pt.list(context='PETRA', server='HISTORY', property=property)
    return d['devices']

def get_value(property, device, depth, stop):
    h=pt.history(address='/PETRA/HISTORY/'+device,property=property, depth=depth, stop=stop)
    return h

# tine has device-property paradigm
# need to map it to relevant higher-level subsystems and parameters
# Temperature
# Alignment
# Alignment->Sensor->X
# Alignment->Sensor->Y
# Beam
# beam->Orbit
# Beam->Qx, Qy
# Beam->ex, ey
# Beam->current
# Beam->nBunches (fillPattern)
# Beam


#PETRA/HISTORY/T_PXN_X/BODENPLATTENMESSUNG

#T_PXN bedeutet: In Strahlrichtung vom Tunnel nach PXN, also NR60.
#PXN_T bedeutet: Von PXN in den Tunnel, also NR139
#T_PXE bedeutet: In Strahlrichtung vom Tunnel nach PXE, also OR60.
#PXE_T bedeutet: Von PXE in den Tunnel, also NR139
#Das sind die Enden der Bodenplatte in den neuen Experimentierhallen.

#Koordinaten:
#x ist horizontal, positiv nach ringaußen
#y ist vertikal, positiv nach oben
#z ist longitudinal, positiv in Strahlrichtung.

#Das gleiche gibt es als
#PETRA/HISTORY/T_SWL_X/BODENSEGMENTMESSUNG  (...SEGMENT...!)

#T_SWL bedeutet: In Strahlrichtung vom Tunnel nach SWL, also SWL38.
#SWR_T bedeutet: In Strahlrichtung von SWR in den Tunnel, also SWR38.
#Dies sind die beiden Messungen an 'normalen' Gebäudefugen.


#DataFrame

def get_data_frame(date, depth, sampling):
    dataFrame = {}
    dataFrame['Temperature'] = {}
    property = 'Temps.Magnets'
    devices = get_device_list(property)
    for dev in devices:
        h=get_value(property=property, device=dev, depth=depth, stop=date + ' 13:00:00')
        dataFrame['Temperature'][dev] = h

    dataFrame['Alignment'] = {}
    property = 'BODENSEGMENTMESSUNG'
    devices = get_device_list(property)
    for dev in devices:
        time.sleep(0.1)
        h=get_value(property=property, device=dev, depth=depth, stop=date + ' 13:00:00')
        dataFrame['Alignment'][dev] = h

    property = 'BODENPLATTENMESSUNG'
    devices = get_device_list(property)
    for dev in devices:
        time.sleep(0.1)
        h=get_value(property=property, device=dev, depth=depth, stop=date + ' 13:00:00')
        dataFrame['Alignment'][dev] = h


    dataFrame['Beam'] = {}
    dataFrame['Beam']['Qx'] = {}
    dataFrame['Beam']['Qx']['unit'] = 'Hz'
    dataFrame['Beam']['Qx']['value'] = 0.0

    return dataFrame

frame = get_data_frame(sys.argv[1],'24hours','')
#print(frame)
json.dump(frame, open(sys.argv[2],'w'))
