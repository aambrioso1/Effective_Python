"""
Item 50: Annotate Class Attributes with __set_name__

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
A useful feature of metaclasses is that metaclasses allow one to modify or annotate properties of a class after
the class is defined but before it is used.   For this approach we used descriptors.  A descriptor class can
provide __get__ and __set__ methods.

Metaclasses allow you to modify class attributes before the class is fully defined.
Descriptors and metaclasses allow for declarative behavorior and runtime inttrospection.
Define __set_name__ on your descriptor classs to allow them to take into account their surrounding 
class and property names.
Avoid memory leaks with the weakref built-in module by having descriptors store data they manipulation 
directly within a class's instance dictionary.
"""


# Example 1:  
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Example 2
class Customer:
    # Class attributes
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# Example 3
cust = Customer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Euclid'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# Example 4
class Customer:
    # Left side is redundant with right side
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

print(20*'*')

# Example 5:  The above is redundant since the name of the class is given in the name of the field (left-side).
"""
 We use a metaclass to avoid this problem.  The metaclass will allow us to hook the class statement directly.

""" 


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


# Example 6:  Database rows sholuld inherit from Meta
class DatabaseRow(metaclass=Meta):
    pass


# Example 7:   We adjust the Field class so that the name can be assigned when a field instance is created
class Field:
    def __init__(self):
        # These will be assigned by the metaclass.
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Example 8
class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


# Example 9
cust = BetterCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Euler'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# Example 10:  Must inherit from DatabaseRow or code will break.
try:
    class BrokenCustomer:
        first_name = Field()
        last_name = Field()
        prefix = Field()
        suffix = Field()
    
    cust = BrokenCustomer()
    cust.first_name = 'Mersenne'
except:
    logging.exception('Expected')
else:
    assert False


# Example 11:   The solution is to use the __set_name__ special method for descriptors.
class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # Called on class creation for each descriptor
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Example 12:  Now it works with having to inherit from a specific parent class or having to use a metaclass.
class FixedCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = FixedCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Mersenne'
print(f'After:  {cust.first_name!r} {cust.__dict__}')

