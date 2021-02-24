"""
Item 46: Use Descriptors for Reusable @property Methods

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


# Example 1:  Examples 1 to 4 show a that @property decorator is tedious because code is not reusable.
# Each new property must be adding again even though the method _check_grade is the same.
class Homework:
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._grade = value


# Example 2
galileo = Homework()
galileo.grade = 95
assert galileo.grade == 95


# Example 3
class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')


# Example 4
    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

galileo = Exam()
galileo.writing_grade = 85
galileo.math_grade = 99

assert galileo.writing_grade == 85
assert galileo.math_grade == 99


print('\n'+10*'*'+'Code in asterisk block is a first try but doesn\'t work'+10*'*')

# Example 5:  
class Grade:
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

class Exam:
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


# Example 6
exam = Exam()
exam.writing_grade = 40


# Example 7
Exam.__dict__['writing_grade'].__set__(exam, 40)


# Example 8
exam.writing_grade


# Example 9
Exam.__dict__['writing_grade'].__get__(exam, Exam)


# Example 10:    
class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._value = value


# Example 11
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)


# Example 12
second_exam = Exam()
second_exam.writing_grade = 75
print(f'Second {second_exam.writing_grade} is right')
print(f'First  {first_exam.writing_grade} is wrong; '
      f'should be 82')

print(74*'*','\n')

# Example 13:  The problem is that a single Grade instance is constructed once and 
# shared across all the Exam instances.  To solve this problem the Grade class needs
# to keep track of its value for each Exam instance.  

class Grade:
    def __init__(self):
        self._values = {} # Defines the dictionary used to keep track of values for Exam instances.

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._values[instance] = value


# Example 14:  The implimentation in Example 13 leaks memory.   The solutilns it use the WeakKeyDictionary 
# in the weakref built-in module.   The makes sure _values dictionary will be empty when Exam instances are
# no longer in use.

from weakref import WeakKeyDictionary

class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._values[instance] = value


# Example 15
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'First  {first_exam.writing_grade} is right')
print(f'Second {second_exam.writing_grade} is right')