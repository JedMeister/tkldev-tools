import time
from sys import exit

__VERBOSITY__ = 0
VERBOSITIES = ('info', 'warning', 'error', 'fatal')

def set_verbosity(verbosity):
    global __VERBOSITY__
    if verbosity not in ('info', 'warning', 'error', 'fatal'):
        raise ValueError('Invalid verbosity "{}"'.format(verbosity))
    __VERBOSITY__ = VERBOSITIES.index(verbosity)

def get_verbosity():
    return __VERBOSITY__

def log(level, msg, prefix=None, seperator='--'):
    if VERBOSITIES.index(level) >= __VERBOSITY__:
        print(level, '<=', __VERBOSITY__)
        if prefix is None:
            prefix = time.strftime('%Y/%m/%d %H:%M:%S')
        print(level.upper(), prefix, seperator, msg)

def info(msg, prefix=None, seperator='--'):
    log('info', msg, prefix, seperator)

def warning(msg, prefix=None, seperator='--'):
    log('warning', msg, prefix, seperator)

def error(msg, prefix=None, seperator='--'):
    log('error', msg, prefix, seperator)

def fatal(msg, prefix=None, seperator='--', returncode=None):
    log('fatal', msg, prefix, seperator)
    exit(returncode or 1)
