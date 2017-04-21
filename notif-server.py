import socketserver
import struct
import json
from subprocess import check_call
import notify2
import sys

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
            sys.stderr.write('Unknown urgency "%s"' % urgency)
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

        notify(**self.data)

if __name__ == "__main__":
    HOST, PORT = "", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), NotifSock)
    print('Listening on {}:{}'.format(HOST, PORT))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
