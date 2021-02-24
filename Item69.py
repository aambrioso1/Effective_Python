"""
Item 69: Use decimal When Precision is Paramount

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
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)


# Example 2
print(round(cost, 2))


# Example 3
from decimal import Decimal

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)


# Example 4
print(Decimal('1.45'))
print(Decimal(1.45))


# Example 5
print('456')
print(456)


# Example 6
rate = Decimal('0.05')
seconds = Decimal('5')
small_cost = rate * seconds / Decimal(60)
print(small_cost)


# Example 7
print(round(small_cost, 2))


# Example 8
from decimal import ROUND_UP

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {cost} to {rounded}')


# Example 9
rounded = small_cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {small_cost} to {rounded}')
