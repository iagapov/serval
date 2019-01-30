# read archive channels from tine and prepare .json files to be later injested by the db
import PyTine as pt
from datetime import datetime
import json


'''
# attaching listener
def cb(id,cc,d):
    print(d['timestamp'])
    print(d['data'])


lid=pt.attach(address='/PETRA/Idc/Buffer-0',property='I',callback=cb)
'''

data = {}

d=pt.list(context='PETRA', server='HISTORY')
temp_channels = [t for t  in d['properties'] if t.lower().find('temp') >= 0]

for ch in temp_channels:
    print('reading channel: ' + ch)
    try:
        h=pt.history(address='/PETRA/HISTORY/keyword',property=ch,depth='2400hours', stop='30.11.2018 13:00:00')
        data[ch] = {'data':h}
        print('ok')
    except:
        print('No channel data in archive')

data['tags'] = ['petra','archive','history']

#h=pt.history(address='/PETRA/HISTORY/keyword',property='CurDC',depth='2400hours', stop='30.11.2018 13:00:00')

[datetime.utcfromtimestamp(t[1]) for t in h]

json.dump(data, open('injest.json','w'))
