# read archive channels from tine and prepare .json files to be later injested by the db
import PyTine as pt
from datetime import datetime
import json
import sys

'''
# attaching listener
def cb(id,cc,d):
    print(d['timestamp'])
    print(d['data'])


lid=pt.attach(address='/PETRA/Idc/Buffer-0',property='I',callback=cb)
'''

data = {}

d=pt.list(context='PETRA', server='HISTORY',property='Temps.Magnets')
#temp_channels = [t for t  in d['properties'] if t.lower().find('temp') >= 0]
devices = d['devices']
import time

#h=pt.history(address='/PETRA/HISTORY/keyword',property=temp_channels[0],depth='2400hours', stop='30.11.2018 13:00:00')
#data[temp_channels[0]] = h
#time.sleep(2)
#h=pt.history(address='/PETRA/HISTORY/keyword',property=temp_channels[1],depth='2400hours', stop='30.11.2018 13:00:00')
#data[temp_channels[1]] = h

for ch in devices:
    print('reading channel: ' + ch)
    try:
        time.sleep(0.1)
        h=pt.history(address='/PETRA/HISTORY/'+ch,property='Temps.Magnets',depth='2400hours', stop='30.12.2018 13:00:00')
        time.sleep(0.1)
        data[ch] = {'data':h}
        print('ok')
    except Exception as e:
        print('No channel data in archive')
        print(e)

data['tags'] = ['petra','archive','history']

#h=pt.history(address='/PETRA/HISTORY/keyword',property='CurDC',depth='2400hours', stop='30.11.2018 13:00:00')

#[datetime.utcfromtimestamp(t[1]) for t in h]

json.dump(data, open(sys.argv[1],'w'))
