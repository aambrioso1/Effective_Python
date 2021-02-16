#!/usr/bin/env PYTHONHASHSEED=1234 python3

"""
Item 42: Prefer Public Attributes Over Private Ones

"""

# Reproduce book environment
import random
random.seed(1234)

import logging # Used for exception handling
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
There are only two types of visibility in Python for class attributes: public and private
Some things to remember:
Private atrributes are not rigorously enforced.
Use the documentation for protected fields rather than trying to control access with private
attributes.
Use private attributes only to control naming conflicts.
Document protected fields carefully.

"""
# Example 1:  Indicate a private field by prefixed it with a double underscore.
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


# Example 2:  Public attributes can be directly accessed by anyone
foo = MyObject()
assert foo.public_field == 5


# Example 3:  Note that the foo class has access to its own private field
assert foo.get_private_field() == 10


# Example 4:  You cannot access a private field directly from outside the class.
try:
    foo.__private_field
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


# Example 6:  A subclass cannot access its parent class's private fields
try:
    class MyParentObject:
        def __init__(self):
            self.__private_field = 71
    
    class MyChildObject(MyParentObject):
        def get_private_field(self):
            return self.__private_field
    
    baz = MyChildObject()
    baz.get_private_field()
except:
    logging.exception('Expected')
else:
    assert False


# Example 7:   Note that the reason that the subclass access to a private field fails
# is that the field is prefix with the name of the class it was created in.
# Understanding this makes it is to access a parent class's private field if you need to.
assert baz._MyParentObject__private_field == 71


# Example 8:  Shows how the private fiels attributes are stored
print(baz.__dict__)


# Example 9
class MyStringClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == '5'


# Example 10
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5


# Example 11
class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())         # Updated

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)  # Not updated


# Example 12:  Problem with private field renamed by subclasses.
try:
    foo = MyIntegerSubclass(5)
    foo.get_value()
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
class MyStringClass:
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned in
        # the object it should be treated as immutable.
        self._value = value


    def get_value(self):
        return str(self._value)
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return self._value

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5


# Example 14:   Use private fields only when you are concerned that names will conflict because a 
# particular name is commonly used.
class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

# Example 15: Use the double underscore and a private attribute to avoid a nameing conflict.
# This can be useful when working with unknown API's and common using common names.
a = Child()
print(f'{a.get()} and {a._value} should be different')

class ApiClass:
    def __init__(self):
        self.__value = 5 # double underscore

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

a = Child()
print(f'{a.get()} and {a._value} should be different')

#  We can access the "private" attribute directly.
print(f'a._ApiClass__value is {a._ApiClass__value} just like a.get()!')