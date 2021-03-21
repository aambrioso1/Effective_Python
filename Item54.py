"""
Item 54: Use Lock to Prevent Data Races in Threads

"""

"""
The GIL does not protect racing data between threads.   The programmer must do this.
Data structures can be corrupted if you allow multiple threads to modify the same objects
with mutual-exclusion locks (mutexes)
The Lock class from the threading built-in module will prevent this kind of data corruption.

The code shows what can go wrong and how to fix the problem with an example simulating sensor being monitored 
on multiple threads running in parallel.
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


# Example 1:  We implement a counter class to count sensor measurement for sensor running on separate
# worker threads.
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


# Example 2:  The function monitors a group of sensor and increments to total count 
# each time it takes a reading from one.
def worker(sensor_index, how_many, counter):
    # I have a barrier in here so the workers synchronize
    # when they start counting, otherwise it's hard to get a race
    # because the overhead of starting a thread is high.
    BARRIER.wait()
    for _ in range(how_many):
        # Read from the sensor
        # Nothing actually happens here, but this is where
        # the blocking I/O would go.
        counter.increment(1)


# Example 3:  We run 5 workers in parallel.
from threading import Barrier
BARRIER = Barrier(5)
from threading import Thread

how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')


# Example 4:   This line of code operates as shown in example 5.   Python threads can be interrupted
# between the operation show in example 5.
counter.count += 1


# Example 5
value = getattr(counter, 'count')
result = value + 1
setattr(counter, 'count', result)


# Example 6:   This example shows what can happen when threads are interrupted.
# Running in Thread A
value_a = getattr(counter, 'count')
# Context switch to Thread B
value_b = getattr(counter, 'count')
result_b = value_b + 1
setattr(counter, 'count', result_b)
# Context switch back to Thread A
result_a = value_a + 1
setattr(counter, 'count', result_a)


# Example 7:  We use the Lock class and a with statement to adquire and release the lock.
from threading import Lock

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


# Example 8:  Now the code works as expected.
BARRIER = Barrier(5)
counter = LockingCounter()

for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')