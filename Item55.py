"""
Item 55:  Use Queue to Coordinate Work Between Threads

"""

"""
Pipelines are useful for concurrent work especially I/O-bound programs.   They can run
concurrently using Python threads.

There are many problems with building concurrent pipelines like:  busy waiting, how to tell workers to stop, 
and potential memory overloads.

The built-in Queue class has all the facilities needed to build robust pipelines:  blocking operations, buffer
sizes, and joining.


Queues work well for linear pipelines.   They are better tools for other situations.
See Item 60:  Achieve Highly Concurrent I/O with Coroutines.
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

# Example 1:  We build a pipeline to simulate a pipeline involving downloading images from a camera, resizing them, 
# and uploading them to an online gallery.   The pipeline can be parallelized as follows.    
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item


# Example 2:  We use deque from the collections module an Lock from the threading module to set up the queue in
# thread-safe way.
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()


# Example 3
    def put(self, item):
        with self.lock:
            self.items.append(item)


# Example 4
    def get(self):
        with self.lock:
            return self.items.popleft()


# Example 5:  The Worker class takes input from the queue applies a function to it 
# and puts the result back into a queue ready for the next phase of the process.
# It also tracks how many times the work has checked for new input and how much worki
#has been completed.

from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0


# Example 6:  This methed checks for an item in the queue and if it finds one it executes func, 
# on it, passes the result to the out_queue and increments the work_done count.
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # No work to do
            except AttributeError:
                # The magic exit signal
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


# Example 7:   Now we set up the queues for each stage and start the different stages concurrently.
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


# Example 8
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())


# Example 9
while len(done_queue.items) < 1000:
    # Do something useful while waiting
    time.sleep(0.1)

# Stop all the threads by causing an exception in their
# run methods.
for thread in threads:
    thread.in_queue = None # Receives magic signal
    thread.join()


# Example 10:  Shows that worker functions are getting bogged down raising and catching
# exceptions.

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f'Processed {processed} items after '
      f'polling {polled} times')

# Example 11:   Need to solve the several problems:  backed up pipelines, making sure input work is complete,
# worker run methods may execute forever, and a backup can crash the program arbitrarily.
# The solution is to use the Queue class in the built-in queue module.
from queue import Queue

my_queue = Queue()

def consumer():
    print('Consumer waiting')
    my_queue.get()              # Runs after put() below
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()


# Example 12:  Together with Example 11, these examples illustrate the workflow control.
print('Producer putting')
my_queue.put(object())          # Runs before get() above
print('Producer done')
thread.join()


# Example 13:  Queue allows the programmer to specify a maximum amount of pending work to allow 
# phases between two.
# The buffer size cause calls to put to block when the queue is full.
my_queue = Queue(1)             # Buffer size of 1

def consumer():
    time.sleep(0.1)             # Wait
    my_queue.get()              # Runs second
    print('Consumer got 1')
    my_queue.get()              # Runs fourth
    print('Consumer got 2')
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()


# Example 14:  This example and the next show the workflow as the phases coordinate their work.
my_queue.put(object())          # Runs first
print('Producer put 1')
my_queue.put(object())          # Runs third
print('Producer put 2')
print('Producer done')
thread.join()


# Example 15:  the task_done method lets you wait for a phase's input queue to drain so we know
# when an item is finished without using done_queue.
in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get()       # Done second
    print('Consumer working')
    # Doing work
    print('Consumer done')
    in_queue.task_done()        # Done third

thread = Thread(target=consumer)
thread.start()


# Example 16:  Now the join command will wait for in_queue to finish so polling is unnecessary.
print('Producer putting')
in_queue.put(object())         # Done first
print('Producer waiting')
in_queue.join()                # Done fourth
print('Producer done')
thread.join()


# Example 17:   We define a close method that adds a SENTINEL to indicate that the will be no more input after it.
class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)


# Example 18:  This function looks for the SENTINEL and stopes iteration when its found.
    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()


# Example 19:  No the worker thread is redefined so that it coordinates with the CloseableQueue class.
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


# Example 20:  Now we create the worker threads using the new classes.
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]


# Example 21:  We start the worker threads, send the stop signal after input to the first phase is finished.
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object()) # Download is the first phase.

download_queue.close() # This sends the SENTINEL signal.


# Example 22:  Now we can coordinate the action of the workers by joining an closing them in order.
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')

for thread in threads:
    thread.join()


# Example 23:  This adds one more feature:  have multiple workers per thread to increase I/O parallelsim.
def start_threads(count, *args):  # A helper function to start multiple threads.
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):  # A helper function to stop multiple threads.
    for _ in threads:
        closable_queue.close()

    closable_queue.join()

    for thread in threads:
        thread.join()


# Example 24:  Now we connect all of the pieces together.



download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

download_threads = start_threads(
    3, download, download_queue, resize_queue)
resize_threads = start_threads(
    4, resize, resize_queue, upload_queue)
upload_threads = start_threads(
    5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), 'items finished')