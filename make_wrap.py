

import sys
import socket
import struct
import json
from os.path import basename
from os import getcwd
from subprocess import Popen
from time import time

HOST, PORT = ('192.168.1.89', 9999)

title = socket.gethostname() + ':' + basename(getcwd())
args = ['make'] + sys.argv[1:]

before = time()

proc = Popen(args)
#XXX Proc throws CalledProcess error sometimes, but isn't handled
ret = proc.wait()

after = time()

data = json.dumps({
    'urgency': 'critical' if ret else 'normal',
    'expire_time': 0,
    'app_name': title,
    'icon': None,
    'category': None,
    'summary': 'Fail' if ret else 'Success',
    'body': 'Took %.2f seconds' % (after-before),
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
