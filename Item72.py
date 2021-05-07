"""
Item 72:  Consider Searching Sorted Sequences with bisect


Searching sorted data contained in a list takes linear time using the index method
or a for loop with simple comparisons.

The bisect built-in module's bisect_left function takes logarithmic time to
search for values in sorted lists.  This is orders of magnidude foaster then other 
approaches

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


# Example 1:   We create a sorted list and look for where 91243 fits in.
data = list(range(10**5))
index = data.index(91234)
assert index == 91234


# Example 2:  We do a linear scan to figure where to install goal.
def find_closest(sequence, goal):
    for index, value in enumerate(sequence):
        if goal < value:
            return index
    raise ValueError(f'{goal} is out of bounds')

index = find_closest(data, 91234.56)
assert index == 91235

try:
    find_closest(data, 100000000)
except ValueError:
    pass  # Expected
else:
    assert False


# Example 3:  A better way is to used bisect_left from the bisect built-in module.
# The code here returns with the location of the item in the list if it's there or where you want to place.
from bisect import bisect_left

index = bisect_left(data, 91234)     # Exact match
assert index == 91234

index = bisect_left(data, 91234.56)  # Closest match
assert index == 91235


# Example 4:  Now we verify the speed improvement with the timeit built-in module.
import random
import timeit

size = 10**5
iterations = 1000

data = list(range(size))
to_lookup = [random.randint(0, size)
             for _ in range(iterations)]

def run_linear(data, to_lookup): # Uses the index method of the list class for lookup
    for index in to_lookup:
        data.index(index)

def run_bisect(data, to_lookup): # Use the bisect_left method in the bisect built-in module for lookup.
    for index in to_lookup:
        bisect_left(data, index)

# We test both implementations.
baseline = timeit.timeit(
    stmt='run_linear(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'Linear search takes {baseline:.6f}s')

comparison = timeit.timeit(
    stmt='run_bisect(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'Bisect search takes {comparison:.6f}s')

slowdown = 1 + ((baseline - comparison) / comparison)
print(f'{slowdown:.1f}x time')