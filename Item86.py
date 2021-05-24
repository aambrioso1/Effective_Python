"""
Item 86: Consider Module-Scoped Code to Configure Deployment Environments

Requires three programs:
(1) db_connection.py
(2) dev_main.py
(3) prod_main.py

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


# Example 4
# db_connection.py
import sys

class Win32Database:
    pass

class PosixDatabase:
    pass

if sys.platform.startswith('win32'):
    Database = Win32Database
else:
    Database = PosixDatabase