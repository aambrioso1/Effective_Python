"""
Item 66: Consider contextlib and with Statements for Reusable try/finally Behavior

"""

#!/usr/bin/env PYTHONHASHSEED=1234 python3


# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
from threading import Lock

lock = Lock()
with lock:
    # Do something while maintaining an invariant
    pass


# Example 2
lock.acquire()
try:
    # Do something while maintaining an invariant
    pass
finally:
    lock.release()


# Example 3
import logging
logging.getLogger().setLevel(logging.WARNING)

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

