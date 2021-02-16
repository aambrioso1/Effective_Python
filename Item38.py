"""
Item 38:  Accept Functions Instead of Classes for Simple Interfaces 

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


"""
Example 1:  Using a function as a hook.   Works well in Python because functions
are easy to define and because they are first-class objects in Python.   They can be
passed around and referenced like other objects.
"""
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=len)
print(names)


# Example 2
def log_missing():
    print('Key added')
    return 0


# Example 3
from collections import defaultdict

current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
    ('blue', 3),
    ('violet', 1),
    ('white', 2),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))


# Example 4
def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# Example 5
result, count = increment_with_report(current, increments)
assert count == 4
print(result)


# Example 6
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# Example 7
counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method ref
for key, amount in increments:
    result[key] += amount
assert counter.added == 4
print(result)


# Example 8
class BetterCountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)


# Example 9:  Shows the __call__ special method.   The idea is that the class will
# behave as defined by the __call__ special methond when it is called as a function.
# When you need a function to maintain state consider defining a class with a __call__
# method instead of defining a stateful closure.  In other words, since a instance of
# a class will hold on to its state.


counter = BetterCountMissing()
result = defaultdict(counter, current)  # Relies on __call__
print(f'current = {current}')
print(f'increments = {increments}')
for key, amount in increments:
    result[key] += amount

assert counter.added == 4
print(f'result = {result}')
print(f'counter.added: {counter.added}')
