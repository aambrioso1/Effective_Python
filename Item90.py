"""
Item 90:  Consider Static Analysis via typing to Obviate Bugs 

This items uses the following programs:
(1) item_90_example_02.py
(2) item_90_example_04.py
(3) item_90_example_08.py
(4) item_90_example_10.py
(5) item_90_example_12.py
(6) item_90_example_14.py
(7) item_90_example_17.py


Wide variety of options are available.  See:  https://docs.python.org/3/library/typing.html

Some best practices:
Don't use type annotations with new code
Type hints are most useful at the boundaries of a code base.   Type hints complement integration tests.
Don't try for 100% coverage.
Include static analysis as part of an automated build and test system.  Configurations used for type 
checking should be standardized for all collaborators.
As you add type information, check your code.   Others debuggging errors that introduced by type hints
may be more difficult to debug.
Evaluate whether you need type hints at all.

Python has type hinting and special syntax (in the typing built-in module) for annotating variables,
fields, functions, and methods.
Static type checkers can leverage type information to avoid bugs at runtime.
Follow the best practices listed above.

Finally finished!!!

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
try:
    def subtract(a, b):
        return a - b
    
    subtract(10, '5')
except:
    logging.exception('Expected')
else:
    assert False


# Example 3
try:
    def concat(a, b):
        return a + b
    
    concat('first', b'second')
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
class Counter:
    def __init__(self):
        self.value = 0

    def add(self, offset):
        value += offset

    def get(self) -> int:
        self.value


# Example 6
try:
    counter = Counter()
    counter.add(5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
try:
    counter = Counter()
    found = counter.get()
    assert found == 0, found
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
try:
    def combine(func, values):
        assert len(values) > 0
    
        result = values[0]
        for next_value in values[1:]:
            result = func(result, next_value)
    
        return result
    
    def add(x, y):
        return x + y
    
    inputs = [1, 2, 3, 4j]
    result = combine(add, inputs)
    assert result == 10, result  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
try:
    def get_or_default(value, default): 
        if value is not None:
            return value
        return value
    
    found = get_or_default(3, 5)
    assert found == 3
    
    found = get_or_default(None, 5)
    assert found == 5, found  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
class FirstClass:
    def __init__(self, value):
        self.value = value

class SecondClass:
    def __init__(self, value):
        self.value = value

second = SecondClass(5)
first = FirstClass(second)

del FirstClass
del SecondClass


# Example 15
try:
    class FirstClass:
        def __init__(self, value: SecondClass) -> None:  # Breaks
            self.value = value
    
    class SecondClass:
        def __init__(self, value: int) -> None:
            self.value = value
    
    second = SecondClass(5)
    first = FirstClass(second)
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
class FirstClass:
    def __init__(self, value: 'SecondClass') -> None:  # OK
        self.value = value

class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value

second = SecondClass(5)
first = FirstClass(second)