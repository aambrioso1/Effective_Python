"""
Item 66: Consider contextlib and with Statements for Reusable try/finally Behavior


The with statement is used to allow you to reuse logic from try/finally blocks.
The contextlib built-in module provides a contextmanager decorator that makes it easy
to use your function sin with statements.
The value yielded by a context manager is supplied as part of the as part of the with statement.

"""

#!/usr/bin/env PYTHONHASHSEED=1234 python3


# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUTS

# Write all output to a temporary directoryS
import atexit
import gc
import io
import os
import tempfile
"""
TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))

os.chdir(TEST_DIR.name)
print(f'{TEST_DIR.name=}')
print(f'{os.getcwd()=}')

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)
"""

# Example 1:   The first two examples show how a with block is equivalent to the try/finally construction
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


# Example 3:  We use the contextmanager decorator together with a with block 
# to create a region of code with a desired behavior (more debug logging)
import logging
logging.getLogger().setLevel(logging.WARNING)

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')


# Example 4
my_function()


# Example 5:  This function will raise the loging severity level before running the code in the with block
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


# Example 6:   Code in the with block with have all the debug messages and outside the with block
# the debug messages will not not run.
with debug_logging(logging.DEBUG):
    print('* Inside:')
    my_function()

print('* After:')
my_function()
print("**** First working example of the contextmanager is complete! ******")

# Example 7:  A pythonic example of using the with statement with a target.
print(f'{os.getcwd()=}')

with open('my_output.txt', 'w') as handle:
    handle.write('This is some data!')


# Example 8:  We use yield to allow a function to supply values to as targets.

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


# Example 9:  We can set the logging level in the with block and the default level will be restore when we leave the block.
with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug(f'This is a message for {logger.name}!')
    logging.debug('This will not print')


# Example 10
logger = logging.getLogger('my-log')
logger.debug('Debug will not print')
logger.error('Error will print')


# Example 11:  We can change the name of the logger by updating the wiht statement.
with log_level(logging.DEBUG, 'other-log') as logger:
    logger.debug(f'This is a message for {logger.name}!')
    logging.debug('This will not print')