from tine_injest import *

import datetime

year = 2018

d = datetime.date(year,1,1)
for i in range(366):
    if d.year == year:
        day_str = d.strftime('%d.%m.%Y')
        print('getting data for: ', day_str)
        frame = get_data_frame(day_str,'24hours','')

        json.dump(frame, open(sys.argv[2] + day_str + '.json','w'))

    d+=datetime.timedelta(days=1)
