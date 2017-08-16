import argparse
import BaseHTTPServer
import fitbit
import json
import logging
import subprocess

LOG = logging.getLogger('fitbit-req')


class OAuthResponseHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def error(self, code, msg):
        self.send_response(code)
        self.end_headers()
        self.wfile.write('An error occurred: %s', msg)

    def do_GET(self):
        if '?' not in self.path:
            return self.error(400, 'missing query')

        query = dict(
            p.split('=') for p in
            self.path.split('?', 1)[1].split('&')
        )

        if 'code' not in query or 'state' not in query:
            return self.error(400, 'missing code')

        if query['state'] != self.server.state:
            return self.error(400, 'state mismatch')

        self.server.auth_code = query['code']

        self.send_response(200)
        self.end_headers()
        self.wfile.write('Thanks!')

    def log_request(self, *args, **kwargs):
        pass


class Server(BaseHTTPServer.HTTPServer):
    def __init__(self, state, port=3863):
        BaseHTTPServer.HTTPServer.__init__(
            self, ('127.0.0.1', port), OAuthResponseHandler)

        self.state = state
        self.auth_code = None


def parse_args():
    p = argparse.ArgumentParser()

    g = p.add_argument_group('Authentication options')
    g.add_argument('--client', '-C',
                   default='client.json')
    g.add_argument('--token', '-T',
                   default='token.json')
    g.add_argument('--port', '-p',
                   default=3863,
                   type=int)

    g = p.add_argument_group('Logging options')
    g.add_argument('--debug', '-d',
                   action='store_const',
                   const='DEBUG',
                   dest='loglevel')
    g.add_argument('--verbose', '-v',
                   action='store_const',
                   const='INFO',
                   dest='loglevel')

    p.set_defaults(loglevel='WARNING')

    return p.parse_args()


def handle_oauth_redirect(state):
    s = Server(state=state)
    LOG.info('waiting for oauth redirect')
    while True:
        s.handle_request()
        if s.auth_code:
            break

    return s.auth_code


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    with open(args.client) as fd:
        LOG.info('reading client id from %s', args.client)
        client = json.load(fd)

    c = fitbit.Fitbit(client['client_id'], client['client_secret'],
                      redirect_uri='http://localhost:3863')
    url, state = c.client.authorize_token_url()
    subprocess.check_call(['xdg-open', url])

    code = handle_oauth_redirect(state)
    token = c.client.fetch_access_token(code)

    with open(args.token, 'w') as fd:
        LOG.info('writing token to %s', args.token)
        json.dump(token, fd)

if __name__ == '__main__':
    main()
