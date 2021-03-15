"""
Item 51: Prefer Class Decorators Over Metaclasses for Composable Class Extensions

"""

"""


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



# Example 1:  Create a decorator that adds a helper to all the methods in a class that prints arguments,
# returns vallues, and exceptions raised.
from functools import wraps

def trace_func(func):
    if hasattr(func, 'tracing'):  # Only decorate once
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r}, {kwargs!r}) -> '
                  f'{result!r}')

    wrapper.tracing = True
    return wrapper


# Example 2:  We use the decorator
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)


# Example 3
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
else:
    assert False

print(20*'*')  # The print statements help break up the examples.  So the output for the examples is separated.

# Example 4:   The example above has redundant code and changes to the dict superclass won't be decorated unless
# we add code to trace. 
# One way to solve this problem is with metaclasses.

import types

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)

class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass


# Example 5:   This example using the TraceMeta metaclass to avoid the redundate code.
# But won't work if a superclass has already already has a specified metaclass.

class TraceDict(dict, metaclass=TraceMeta):
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
else:
    assert False


# Example 6
try:
    class OtherMeta(type):
        pass
    
    class SimpleDict(dict, metaclass=OtherMeta):
        pass
    
    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except:
    logging.exception('Expected')
else:
    assert False

print(20*'*')

# Example 7:   We solve this problem having OtherMeta inherit from TraceMeta
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = type.__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass

class OtherMeta(TraceMeta): # OtherMeta inherits from TraceMeta
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

class TraceDict(SimpleDict, metaclass=TraceMeta): # Also TraceDict inherits from TraceMeta
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
else:
    assert False

print(20*'*')

# Example 8:  The solutions above won't work if the other metaclass can't be modified or if 
# we used multiple utility metaclasses at the same time.   Metaclasses put too many constraints
# on the class that's being modified.

# We implement a class decorator to a apply "trace_func to all the methods and function of a class by
# moving the core of the TraceMethod.__new__ method to a stand-alone function."
# The code is much shorter too.


def my_class_decorator(klass):
    klass.extra_param = 'hello'
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)


# Example 9
def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass

# Example 10:
@trace
class TraceDict(dict):
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
else:
    assert False


# Example 11:  It works when the class class being decorated alread has a metaclass.
class OtherMeta(type): # A dummy metaclass for testing
    pass

@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
else:
    assert False