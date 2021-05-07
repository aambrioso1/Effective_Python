"""
Item 70: Profile Before Optimizing

Python has two built-in modules for profiling.  On is pure python (profile) and the other is
a C-extension module (cProfile).    The cProfile module is better because it has a minimal effect on
system performance.   The profile module is a high overhead that may impact the performance of the program
you are profiling and skew results.

Slow downs in Python can be obscure.   You should always profile your programs before optimizing.
Use cProfile instead of profile to get more accurate profiling data.
The Profile object's runcall method provides every you need to profile a tree of functions.
The Stats object lets you select and print the subsist of profiling information you need.

Amdahl's law
See https://en.wikipedia.org/wiki/Amdahl%27s_law
The law that shows how the theoretical speed up of a parallalizing a serial process is limited
by the fraction of the process that cannot be parallelized.   The theoretical limit is given 
be 1/(1-p) where p is the fraction of the process time that can be parallelized.

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


# Example 1:  We create an inefficient sort algorithm to profile.
def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


# Example 2:  The key to the insertion sort is the part of the algorithm that decides the insertion point.
# Here we construct an inefficient algorithm.
def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# Example 3:   We create some random data to sort.  THen sort it.
from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


# Example 4:   We create a instance of cProfile and run it on our test sort.
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)


# Example 5:  Methods in the Stats object will allow us to extract useful information from or profile data.
from pstats import Stats

stats = Stats(profiler)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# Example 6:  Now we use a more efficient built-in method to decide the insertion point.
from bisect import bisect_left

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)


# Example 7:  Now we generate data for the new algorithm.
profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()

print("****** Compare the profile data for the two insert methods *******")

# Example 8:  We create a group of functions that work together.   It is difficulty to
# tell where the execution time is spoend using the default outpoint of cProfile.
def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()


# Example 9:  We profile my_program and generate the default output.
profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# Example 10:  We use the print_callers method of the Stats class
# to show which callers are contributing to the profiling inofrmation of each function.
# The profiles shows taht my_utility uses first_func the most.
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers()