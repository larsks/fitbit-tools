import datetime
import sys
import fitbit
import subprocess
import json

with open('token.json') as fd:
    token = json.load(fd)

c = fitbit.Fitbit('228PSK', '77609df138a7680052b525fe6c97ce69',
                  access_token=token['access_token'],
                  refresh_token=token['refresh_token'])

when = datetime.datetime(*(int(x) for x in sys.argv[1].split('-')))
res = c.get_sleep(when)
print json.dumps(res)
