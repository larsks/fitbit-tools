import argparse
import datetime
import fitbit
import json
import logging
import subprocess
import sys

LOG = logging.getLogger('fitbit-sleep')

def datestr(val):
    return datetime.datetime(*(int(x) for x in val.split('-')))

with open('token.json') as fd:
    token = json.load(fd)

def parse_args():
    p = argparse.ArgumentParser()

    g = p.add_argument_group('Authentication options')
    g.add_argument('--client', '-C',
                   default='client.json')
    g.add_argument('--token', '-T',
                   default='token.json')

    g = p.add_argument_group('Logging options')
    g.add_argument('--debug', '-d',
                   action='store_const',
                   const='DEBUG',
                   dest='loglevel')
    g.add_argument('--verbose', '-v',
                   action='store_const',
                   const='INFO',
                   dest='loglevel')

    p.add_argument('date',
                   nargs='?',
                   type=datestr,
                   default=datetime.datetime.today())

    p.set_defaults(loglevel='WARNING')

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    with open(args.client) as fd:
        LOG.info('reading client id from %s', args.client)
        client = json.load(fd)

    with open(args.token) as fd:
        LOG.info('reading token from %s', args.token)
        token = json.load(fd)

    c = fitbit.Fitbit(client['client_id'], client['client_secret'],
                      access_token=token['access_token'],
                      refresh_token=token['refresh_token'])

    res = c.get_sleep(args.date)
    print json.dumps(res)


if __name__ == '__main__':
    main()
