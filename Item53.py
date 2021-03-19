"""
Item 53: Use Threads for Blocking I/O, Avoid for Parallelism

"""

"""
Python threads cannot run in parallel on multiple cores because of the GIL.
Python threads can be useful since the code will appear as if multiple things
are executing at the same time.
System calls will excecute in parallel when using Python threads.
This allows you to use blocking I/O at the same time as computation.
Blocking I/O includes reading and writing to files, interacting with networks, and communicating
devices.
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


# Example 1:  Simple factorization function that creates a generator that yield the factors of number.
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


# Example 2:  We execute factorize serially and time the process.
import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 3:  We use threads to execute factorize "concurrently."   Note that the GIL prevents this from
# being truly concurrent.    There is no gain in time over a serial implementation.
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


# Example 4:  Start the "concurrent" threads.
start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)


# Example 5:  Wait for all the thread to finish (join()) and time the process.
for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 6:   Threading can speed up a program if system calls are involve.    System calls will release the GIL
# and allow the Python code to continue as the system call runs in a thread.
import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)


# Example 7:  A serial example with 5 system call excecute serially.
start = time.time()

for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 8:   We execute system calls in parallel an compute the "helicopter location" in Python
# while system calls run concurrently.   This will save time since the GIL is released after the system call.
# Note I altered the code so to show that even with 20 system calls the program is not slowed down.
# Note that I also slowed down the helicopter location function so the Python code runs longer.
start = time.time()

threads = []
for _ in range(20):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


# Example 9:  The location code here is the Python part of the program.  It will run concurrently
# with the system calls.  Since the system calls will run in parallel the resulting code will be about
# factor of the-number-of-system-calls faster than a serial implemation.
def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)
    for j in range(100000): pass
    sub_end = time.time()
    sub_delta = sub_end - start
    print(f'{i+1}th loc occurred in {sub_delta:.6f} seconds', sub_end, start)
    

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')