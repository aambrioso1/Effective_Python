"""
Item 75: Use repr Strings for Debugging Output

Calling print produces a human-readable string version of a value
Calling repr produces the print string version of the value.
A repr string can often be passed to eval to get back the original value.
%s in format strings produces human-readable strings like str.
%r in format strings produces printable strings like repr.
F-strings produce human-readable strings useless you specify the !r suffix.
THe printable representation of a class instance can be modified by the __repr__
special method.


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


# Example 1: The print statement prints a human-readable string version of the argument
print('foo bar')


# Example 2:   TFAE
my_value = 'foo bar'
print(str(my_value))
print('%s' % my_value)
print(f'{my_value}')
print(format(my_value))
print(my_value.__format__('s'))
print(my_value.__str__())


# Example 3:  This example shows that the output of a print statement does not make clear what the
# type of the output is.  
print(5)
print('5')

int_value = 5
str_value = '5'
print(f'{int_value} == {str_value} ?')


# Example 4:  The repr function returns the printable representation of an object.   For most 
# built-in types the returned value is a valid Python expresion.
# So a == eval(repr(a))

a = '\x07'
print('a:', a)
print('repr(a): ', repr(a))


# Example 5
b = eval(repr(a))
assert a == b


# Example 6:  Using repr will make the differences between types clear.
print(repr(5))
print(repr('5'))


# Example 7:   This is equivalent to Example 6
print('%r' % 5)
print('%r' % '5')

# The !r suffix is the best way to make sure print statements used for debugging
# give is good information about the stuff being printed.
int_value = 5
str_value = '5'
print(f'{int_value!r} != {str_value!r}')


# Example 8:  Printing instance of this class given "opaque" information.
class OpaqueClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 'foo')
print(obj)


# Example 9:  The __repr__ method lets the print statement know what it should print for a class.
# Now the information given by print will be more useful. 
class BetterClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterClass({self.x!r}, {self.y!r})'


# Example 10:   If you can't control an class definition then the __dict__ method will give
# better information about the inputs to a class instatnce.
obj = BetterClass(2, 'bar')
print(obj)


# Example 11
obj = OpaqueClass(4, 'baz')
print(obj.__dict__)