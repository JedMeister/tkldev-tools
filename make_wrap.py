import sys
import socket
import struct
import json
from os.path import basename, isdir, isfile, dirname, abspath, join
from os import getcwd
from subprocess import Popen
from time import time
from glob import glob
import common

stamps_directory = join(getcwd(), 'stamps')
stamp_order = ('bootstrap', 'root.spec', 'root.build', 'root.patched', 'root.sandbox',
               'cdroot', 'product.iso')

prog_dir = dirname(abspath(__file__))
default_config_path = join(prog_dir, 'conf', 'make_wrap_default_config.json')
config_path = join(prog_dir, 'conf', 'make_wrap_config.json')

if not isfile(config_path):
    common.warning("No config found, creating one from defaults")
    if not isfile(default_config_path):
        common.fatal("No default config found!")
    else:
        with open(default_config_path, 'r') as fob1:
            with open(config_path, 'w') as fob2:
                fob2.write(fob1.read())
            fob1.seek(0)
            config = json.load(fob1)
else:
    with open(config_path, 'r') as fob1:
        config = json.load(fob1)

HOST = config['host']
PORT = config['port']

title = config["app_name"].format(hostname=socket.gethostname(),
        current_dir=basename(getcwd()))
args = [config['make_cmd']] + sys.argv[1:]

before = time()

proc = Popen(args)
#XXX Proc throws CalledProcess error sometimes, but isn't handled
ret = proc.wait()
after = time()

stamps = list(map(basename, glob(join(stamps_directory, '*'))))
if isfile(join(getcwd(), 'product.iso')):
    stamps.append('product.iso')
if stamps:
    highest_stamp = sorted(stamps, lambda x: stamp_order.index(x))[:-1]
else:
    highest_stamp = 'None'

data = json.dumps({
    'urgency': config['urgency_bad'] if ret else config['urgency_good'],
    'expire_time': config['expire_time'],
    'app_name': title,
    'icon': config['icon'],
    'category': config['category'],
    'summary': (config['summary_bad'] if ret else
        config['summary_good']).format(exit_code = ret),
    'body': config['body'].format(time_elapsed=after-before,
        highest_stamp=highest_stamp),
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
