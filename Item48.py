"""
Item 48: Validate Subclasses with __init_subclass__

"""

"""
Metaclasses can be used to inspect or modify a class after it's defined but before its
created.   Can be more heavyweight than needed
The __init_subclass__ method introduced in Python 3.6 ensures that subclasses are well-formed
at the time they are defined and before their type are constructed.
Be sure to call super()__init_subclass__ from within your classes's __init_subclass__ definition 
to ennable validation in multiple layers of classes and multiple inheritance.

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


# Example 1:  Shows that the metaclass has access to class and parent class information as each is
# created.
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        global print
        orig_print = print
        print(f'* Running {meta}.__new__ for {name}')
        print('Bases:', bases)
        print = pprint
        print(class_dict)
        print = orig_print
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass
print(30*'*')

# Example 2:  We use metaclass to validate all parameters of an associated class before its defined.
# In the example we verify that the child of the Polygon class has at least 3 sides.

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate subclasses of the Polygon class
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None  # Must be specified by subclasses

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260
print(f'Nonagon.interior_angles() = {Nonagon.interior_angles()}')

# Example 3
try:
    print('Before class')
    
    class Line(Polygon):
        print('Before sides')
        sides = 2
        print('After sides')
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False

print(30*'*')

# Example 4:  A better and simpler way to accomplish this task with Python 3.6+ is to use the 
# __init_subclass__ special class method.   
class BetterPolygon:
    sides = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720


# Example 5
try:
    print('Before class')
    
    class Point(BetterPolygon):
        sides = 1
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False

print(30*'*')

# Example 6:  This example adds a second metaclass to show that you can only specify
# one metaclass per class definition.  In the example we use a second metaclass to check if the polygon
# is filled with the right color.

class ValidateFilled(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate subclasses of the Filled class
        if bases:
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return type.__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidateFilled):
    color = None  # Must be specified by subclasses


# Example 7:  This returns a cryptic error message because we are using two metaclasses.
try:
    class RedPentagon(Filled, Polygon):
        color = 'blue'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


# Example :  We can fix the problem with a complex heirarchy of metaclass type definitions.
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None  # Must be specified by subclasses

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # Must be specified by subclasses


# Example 9
class GreenPentagon(FilledPolygon):
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)


# Example 10
try:
    class OrangePentagon(FilledPolygon):
        color = 'orange'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
try:
    class RedLine(FilledPolygon):
        color = 'red'
        sides = 2
except:
    logging.exception('Expected')
else:
    assert False

print(30*'*')

# Example 12:  Using the special __init_subclass__ and super() we can solve the problem, allow composibility,
# and reduce the complexity of the code.

class Filled: 
    color = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('Fills need a valid color')


# Example 13:  Now the classes Filled and BetterPolygon can be composed to create polygon classes with appropriate
# validation and easier clearer code.

class RedTriangle(Filled, BetterPolygon):
    color = 'red'
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, BetterPolygon)


# Example 14
try:
    print('Before class')
    
    class BlueLine(Filled, BetterPolygon):
        color = 'blue'
        sides = 2
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 15
try:
    print('Before class')
    
    class BeigeSquare(Filled, BetterPolygon):
        color = 'beige'
        sides = 4
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 16:   The __init_subclass__ method also works in complex cases like diamond inheritance.
# Top, Left, Right, and Bottom form and diamond inheritance pattern.   But Top._init_subclass__ is 
# only class once when each child class is created.

class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Top for {cls}')

class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Left for {cls}')

class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Right for {cls}')

class Bottom(Left, Right):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Bottom for {cls}')
