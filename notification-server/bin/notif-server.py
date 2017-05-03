import socketserver
from argparse import ArgumentParser
import struct
import json
from subprocess import check_call
import notify2
from os import readlink
from os.path import abspath, join, dirname, islink
import sys

# Make sure common is in python path
if islink(abspath(__file__)):
    lib = join(dirname(abspath(readlink(abspath(__file__)))), "lib"))
else:
    lib = join(dirname(abspath(__file__)), "lib")
sys.path.append(lib)

import common

urgency_map = {
    'low': notify2.URGENCY_LOW,
    'normal': notify2.URGENCY_NORMAL,
    'critical': notify2.URGENCY_CRITICAL
}

def notify(summary='', body='', urgency='low', expire_time=None, app_name='',
        icon='', category=''):
    notify2.init(app_name)
    notification = notify2.Notification(summary, body)#, icon)
    if urgency:
        if not urgency in urgency_map:
            error('Unknown urgency "{}" given'.format(urgency))
            info('valid urgencies are ("low", "normal" or "critical")')
        else:
            notification.set_urgency(urgency_map[urgency])
    if not expire_time is None:
        notification.set_timeout(expire_time)
    if category:
        notification.set_category(category)
    notification.show()

class NotifSock(socketserver.BaseRequestHandler):
    """
    Notification request handler class for our server.
    """

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def handle(self):
        # self.request is the TCP socket connected to the client
        size = struct.unpack('Q', self.request.recv(8))[0]
        self.data = json.loads(self.request.recv(size))
        common.info('{} -> {}'.format(self.client_address, self.data))
        notify(**self.data)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-b', '--host', default='')
    parser.add_argument('-p', '--port', default=9999, type=int)
    parser.add_argument('-v', '--verbosity', default='warning', choices =
            common.VERBOSITIES)
    args = parser.parse_args()

    HOST, PORT = args.host, args.port

    common.set_verbosity(args.verbosity)

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), NotifSock)
    print('Listening on {}:{}'.format(HOST, PORT))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
