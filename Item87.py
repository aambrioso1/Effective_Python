"""
Item 87: Define a Root Exception to Insulate Callers from APIs

"When you are defining a modules API, the exceptions you raise are just as much a part of your interface
as the functions and classes your define."

Define root excepts for modules to insulate API consumers from an API
Catching root exceptions can help find bugs in code that consumes an API
Catching exceptions with Python's exception base class can help find bug in an API
Intermediate root exceptions can add more specific type of more scalable code.


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
# my_module.py
def determine_weight(volume, density):
    if density <= 0:
        raise ValueError('Density must be positive')

try:
    determine_weight(1, 0)
except ValueError:
    pass
else:
    assert False
print('******* End of Example 1 ********')

# Example 2
# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """There was a problem with a provided density value."""

class InvalidVolumeError(Error):
    """There was a problem with the provided weight value."""

def determine_weight(volume, density):
    if density < 0:
        raise InvalidDensityError('Density must be positive')
    if volume < 0:
        raise InvalidVolumeError('Volume must be positive')
    if volume == 0:
        density / volume


# Example 3
class my_module:
    Error = Error
    InvalidDensityError = InvalidDensityError

    @staticmethod
    def determine_weight(volume, density):
        if density < 0:
            raise InvalidDensityError('Density must be positive')
        if volume < 0:
            raise InvalidVolumeError('Volume must be positive')
        if volume == 0:
            density / volume

try:
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception('Unexpected error')
else:
    assert False

# Example 4
SENTINEL = object()
weight = SENTINEL
try:
    weight = my_module.determine_weight(-1, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception('Bug in the calling code')
else:
    assert False

assert weight is SENTINEL

print('********** End of Example 4 ***********')
# Example 5
try:
    weight = SENTINEL
    try:
        weight = my_module.determine_weight(0, 1)
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise  # Re-raise exception to the caller
    else:
        assert False
    
    assert weight == 0
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
# my_module.py

class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""


def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError('Density must be positive')


# Example 7
try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
    except my_module.NegativeDensityError:
        raise ValueError('Must supply non-negative density')
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise
    else:
        assert False
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class WeightError(Error):
    """Base-class for weight calculation errors."""

class VolumeError(Error):
    """Base-class for volume calculation errors."""

class DensityError(Error):
    """Base-class for density calculation errors."""