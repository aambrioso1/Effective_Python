"""
Item 69: Use decimal When Precision is Paramount

Python has built-in data types for practically every type of numerical value.

The Decimal class is ideal for situtations that require high precision and control over
rounding behavior.

Pass str instances to the Decimal constructor instead of float instatnces if you are compute
exact values

Consider the Fraction class for representing rational numbers with no limit ot the precision.

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


# Example 1:  Interesting example that show that the built-in float type can lead to rounding errors.
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)


# Example 2
print(round(cost, 2))


# Example 3:   The decimal module solve this problem.  It takes calculations out to 28 decimal places.
from decimal import Decimal

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)

# Example 4:   Decimal instance can be give values as a str or as a int or float.  Using string avoids the loss
# of precision inherent in the Python float type.
print(Decimal('1.45'))
print(Decimal(1.45))


# Example 5:  It is not a problem with the integer type.
print('456')
print(456)


# Example 6
rate = Decimal('0.05')
seconds = Decimal('5')
small_cost = rate * seconds / Decimal(60)
print(small_cost)


# Example 7
print(round(small_cost, 2))


# Example 8:   The quantize method along with ROUND_UP will round value up based on a defined minimum quantity.
from decimal import ROUND_UP

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {cost} to {rounded}')


# Example 9
rounded = small_cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {small_cost} to {rounded}')
