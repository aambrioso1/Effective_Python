"""
Item 47: Use __getattr__, __getattribute__, and __set__attr__ for Lazy Attributes

Use __getattr__ and __setattr__ to lazily load and save attributes for an object.
Understand __getattr__ only gets called when accessing a missing attribute while
__getattribute__ gets called every time any attribute is accessed.
Use methods from super(), the object class, to access instance attributes.

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
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value


# Example 2:  This example illustrates that if an attribute can't be found, foo in example,
# the __getattr__ method will be called.   The acts as hook to allow the missing attribute to be defined.
data = LazyRecord()
print('Before:', data.__dict__)
print('foo:   ', data.foo)
print('After: ', data.__dict__)


# Example 3
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* Called __getattr__({name!r}), '
              f'populating instance dictionary')
        result = super().__getattr__(name)
        print(f'* Returning {result!r}')
        return result

# Added code here to show that __getattr__ is called once for each new attribute.
# After the first call the attribute is added to the dictionary and __getattr__
# is no longer used.
data = LoggingLazyRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo1)
print('First foo again', data.foo1)
print('Second foo: ', data.foo2)
print('Second foo again: ', data.foo2)
print('After: ', data.__dict__)


# Example 4:  The __getattribute__ object hook is called every time an attribute is accessed
# on an object even where it does not exist in the attribute dictionary.
# This allows hte coded to check global transaction states.
# The operation can impact performance.
class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'* Found {name!r}, returning {value!r}')
            return value
        except AttributeError:
            value = f'Value for {name}'
            print(f'* Setting {name!r} to {value!r}')
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)


# Example 5:  Raise an exception if a property should not exist.
try:
    class MissingPropertyRecord:
        def __getattr__(self, name):
            if name == 'bad_name':
                raise AttributeError(f'{name} is missing')
            value = f'Value for {name}'
            setattr(self, name, value)
            return value
    
    data = MissingPropertyRecord()
    assert data.foo == 'Value for foo'  # Test this works
    data.bad_name
except:
    logging.exception('Expected')
else:
    assert False


# Example 6;  Use hasattr built-in function to determine when a property exists 
# and the getattr built-in function to retrieve property values
data = LoggingLazyRecord()  # Implements __getattr__
print('Before:         ', data.__dict__)
print('Has first foo:  ', hasattr(data, 'foo'))
print('After:          ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))


# Example 7:  When __getattribute__ is implemented the class will call the method
# each time hasattr or getattr is used with an instance.
data = ValidatingRecord()  # Implements __getattribute__
print('Has first foo:  ', hasattr(data, 'foo'))
print('Has second foo: ', hasattr(data, 'foo'))
print('Has foobar: ', hasattr(data, 'foobar'))
print('Has first foo:  ', hasattr(data, 'foo'))
print('First foobar:  ', data.foobar)
print('Has first foobar:  ', hasattr(data, 'foo'))
print('Dict after:         ', data.__dict__)
print(20*'*')

# Example 8:  Since the __setattr__ method is always called when an attribute is assigned to an instance
# it can be used as a hook to push data back to a database when values are assigned to the instance.
class SavingRecord:
    def __setattr__(self, name, value):
        # Save some data for the record
        pass
        super().__setattr__(name, value)


# Example 9:  Here __setattr__ is called on each attribute assignment.
class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* Called __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)

data = LoggingSavingRecord()
print('Before: ', data.__dict__)
data.foo = 5
print('After:  ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)


# Example 10: The __getattribute__ method here causes an infinite recursion since the method
# accesses self.data which cause _getattribute__ to run again and again.
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        return self._data[name]


# Example 11
try:
    data = BrokenDictionaryRecord({'foo': 3})
    data.foo
except:
    logging.exception('Expected')
else:
    assert False


# Example 12:  To avoid the recursion use super().__getattribute__ .
class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        # Prevent weird interactions with isinstance() used
        # by example code harness.
        if name == '__class__':
            return DictionaryRecord
        print(f'* Called __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryRecord({'foo': 3})
print('foo: ', data.foo)