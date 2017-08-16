import datetime
import sys
import fitbit
import subprocess
import json
import logging

logging.basicConfig(level='DEBUG')

with open('token.json') as fd:
    token = json.load(fd)

c = fitbit.Fitbit('228PSK', '77609df138a7680052b525fe6c97ce69',
                  access_token=token['access_token'],
                  refresh_token=token['refresh_token'])

date1 = datetime.datetime(*(int(x) for x in sys.argv[1].split('-')))
date2 = datetime.datetime(*(int(x) for x in sys.argv[2].split('-')))
res = c.get_sleep_range(date1, date2)
print json.dumps(res)
