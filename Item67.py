"""
Item 67: Use datetime Instead of time for Local Clocks 


Two ways to accomplish time zone conversions
(1)  the built-in time module which is error prone
(2)  the built-in datetime with support from the open-source package pytz (Python time zone)

Avoid the built-in time module for converting different time zones
Use the built-in datetime module with the open-source the pytz module
Always se UTC to represent time and converted to local time as the final step

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


# Example 1:  Demonstrate using the time module to convert a UNIX timestamp (seconds since the UUNIX epoch in UTC) to
# the host computer's time zone 
import time

now = 1619303700
local_tuple = time.localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = time.strftime(time_format, local_tuple)
print(f'{time_str=}')


# Example 2:  Convert computer time to UTC
time_tuple = time.strptime(time_str, time_format)
utc_now = time.mktime(time_tuple)
print(f'{utc_now=}')


# Example 3:  The time module depends on who underlying C functions work on the host system which makes it
# unreliable.
import os

if os.name == 'nt':
    print("This example doesn't work on Windows")
else:
    parse_format = '%Y-%m-%d %H:%M:%S %Z'
    depart_sfo = '2019-03-16 15:45:16 PDT'
    time_tuple = time.strptime(depart_sfo, parse_format)
    time_str = time.strftime(time_format, time_tuple)
    print(time_str)


# Example 4
try:
    arrival_nyc = '2019-03-16 23:33:24 EDT'
    time_tuple = time.strptime(arrival_nyc, time_format)
except:
    logging.exception('Expected')
else:
    assert False


# Example 5:   The datetime module is better:  Convert present time to UTC.
from datetime import datetime, timezone

now = datetime(2021, 4, 24, 18, 35, 00)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print('Example 5')
print(now_local)


# Example 6
time_str = '2021-04-24 18:50:00'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = time.mktime(time_tuple)
print(utc_now)


# Example 7:   The default Python installation only has time zone information for UTC
# Convert a NY flight arrival time to UTC
import pytz # The open-source module contains a full database of every time zone you may need.

# For online documentation see https://pythonhosted.org/pytz/

arrival_nyc = '2019-03-16 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(f'utc_dt = {utc_dt}')


# Example 8:  Now convert to San Franscisco local time
pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(f'sf_dt = {sf_dt}')


# Example 9:  Or local time in Nepal
nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(f'nepal_dt = {nepal_dt}')