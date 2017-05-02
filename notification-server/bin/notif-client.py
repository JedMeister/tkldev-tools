import argparse
import socket
import struct
import json
import sys

# Create a socket (SOCK_STREAM means a TCP socket)
parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port', type=int)
parser.add_argument('-u', '--urgency', default='low', help='low, normal or critical')
parser.add_argument('-t', '--expire-time', help='timeout in millis')
parser.add_argument('-a', '--app-name', type=str,
        default='notification-server', help='App name for icon')
parser.add_argument('-i', '--icon', nargs='+', help='Icon filename or stock icon')
parser.add_argument('-c', '--category', nargs='+', help='notif category')
parser.add_argument('summary')
parser.add_argument('body', nargs='?', default='')


args = parser.parse_args()
HOST, PORT = args.host, args.port

data = json.dumps({
    'urgency': args.urgency,
    'expire_time': args.expire_time,
    'app_name': args.app_name,
    'icon': args.icon,
    'category': args.category,
    'summary': args.summary,
    'body': args.body
    }).encode('utf8')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(struct.pack('Q', len(data)))
    sock.sendall(data)

    # Receive data from the server and shut down

finally:
    sock.close()

