import json
import fitbit
import subprocess
import BaseHTTPServer

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

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self, state):
        BaseHTTPServer.HTTPServer.__init__(self,
            ('127.0.0.1', 3863),
            OAuthResponseHandler)

        self.state = state
        self.auth_code = None

with open('client.json') as fd:
    client = json.load(fd)

c = fitbit.Fitbit(client['client_id'], client['client_secret'],
                  redirect_uri='http://localhost:3863')
url, state = c.client.authorize_token_url()
subprocess.check_call(['xdg-open', url])

s = Server(state=state)
while True:
    s.handle_request()
    if s.auth_code:
        break

token = c.client.fetch_access_token(s.auth_code)

with open('token.json', 'w') as fd:
    json.dump(token, fd)

