"""
Item 62: Mix Threads and Coroutines to Ease Transition to asyncio

To transition a large program to asynchio and coroutines it may be necessary to use threads for blocking I/O
and coroutines for asynchronous I/O at the same time.
The asyncio module has "built-in facilties that make this interoperability straightforward.""

The run_in_executor mehtod event loop enables synchronous code to run a coroutine in ThreadPoolExectuor
pools.   This helps top-down migrations.

THe run_until_complete mehtod enoalbes synchronous code to run a coroutine until it finishes.   The 
asychio.run_coroutine_threadsafe function provies the same functionality across thread boundaries.
These help with bottom-up migrations.


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
print(f'{OLD_CWD=}')
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1: We want to merge a log files so we need to check if new data is available and return the next line of input
class NoNewData(Exception):  # We use this exception to let us know there is no new data (See Item 20).
    pass

def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()


# Example 2:  We wrap the funciton above in a while loop so we can turn it into a worker thread.
import time

def tail_file(handle, interval, write_func):
    while not handle.closed:  # Worker thread exits when handle is closed.
        try:
            line = readline(handle) 
        except NoNewData:
            time.sleep(interval) # Wait if there is no data
        else:
            write_func(line) # Callback function to write line to output log (See Item 38).


# Example 3:  Start one worker per input files and unify their output into a single file.
from threading import Lock, Thread

def run_threads(handles, interval, output_path):
    with open(output_path, 'wb') as output:
        lock = Lock() # Need the lock so that writes to output stream will be in order (serialized).
        def write(data):
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


# Example 4
# This is code to simulate the writers to the handles
import collections
import os
import random
import string
from tempfile import TemporaryDirectory

def write_random_data(path, write_count, interval):
    with open(path, 'wb') as f:
        for i in range(write_count):
            time.sleep(random.random() * interval)
            letters = random.choices(
                string.ascii_lowercase, k=10)
            data = f'{path}-{i:02}-{"".join(letters)}\n'
            f.write(data.encode())
            f.flush()

def start_write_threads(directory, file_count):
    paths = []
    for i in range(file_count):
        path = os.path.join(directory, str(i))
        with open(path, 'w'):
            # Make sure the file at this path will exist when
            # the reading thread tries to poll it.
            pass
        paths.append(path)
        args = (path, 10, 0.1)
        thread = Thread(target=write_random_data, args=args)
        thread.start()
    return paths

def close_all(handles):
    time.sleep(1)
    for handle in handles:
        handle.close()

def setup():
    tmpdir = TemporaryDirectory()
    input_paths = start_write_threads(tmpdir.name, 5)

    handles = []
    for path in input_paths:
        handle = open(path, 'rb')
        handles.append(handle)

    Thread(target=close_all, args=(handles,)).start()

    output_path = os.path.join(tmpdir.name, 'merged')
    return tmpdir, input_paths, handles, output_path


# Example 5
def confirm_merge(input_paths, output_path):
    found = collections.defaultdict(list)
    with open(output_path, 'rb') as f:
        for line in f:
            for path in input_paths:
                if line.find(path.encode()) == 0:
                    found[path].append(line)

    expected = collections.defaultdict(list)
    for path in input_paths:
        with open(path, 'rb') as f:
            expected[path].extend(f.readlines())

    for key, expected_lines in expected.items():
        found_lines = found[key]
        assert expected_lines == found_lines, \
            f'{expected_lines!r} == {found_lines!r}'

input_paths = ... # ['Item1.py', 'Item2.py', 'Item3.py', 'Item4.py']
handles = ... # ['Item1.py', 'Item2.py', 'Item3.py', 'Item4.py']
output_path = ... # ['file1', 'file2']

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# Example 6
import asyncio

# On Windows, a ProactorEventLoop can't be created within
# threads because it tries to register signal handlers. This
# is a work-around to always use the SelectorEventLoop policy
# instead. See: https://bugs.python.org/issue33792
policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

"""
Top-down approach:
(1)  Change top function to asynch def
(2)  Wrap all functions that do I/O to use aynchio.run_in_executor.
(3)  Make sure resources and callbacks used run_in_executor are synchronized
using Lock or asynchio.run_time_coroutine_threadsafe.
(4)  Try to eliminate get_event_loop and run_in_executor clall by moving down through
the call hierarchy and converting intermediate functions and methods to coroutines following s
steps 1, 2, and 3.  (EP, p. 284-85)
"""

async def run_tasks_mixed(handles, interval, output_path):
    loop = asyncio.get_event_loop()

    with open(output_path, 'wb') as output:
        async def write_async(data):
            output.write(data)

        def write(data):
            coro = write_async(data)
            future = asyncio.run_coroutine_threadsafe(
                coro, loop)
            future.result()

        tasks = []
        for handle in handles:
            task = loop.run_in_executor(
                None, tail_file, handle, interval, write)
            tasks.append(task)

        await asyncio.gather(*tasks)


# Example 7
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks_mixed(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# Example 8
async def tail_async(handle, interval, write_func):
    loop = asyncio.get_event_loop()

    while not handle.closed:
        try:
            line = await loop.run_in_executor(
                None, readline, handle)
        except NoNewData:
            await asyncio.sleep(interval)
        else:
            await write_func(line)


# Example 9
async def run_tasks(handles, interval, output_path):
    with open(output_path, 'wb') as output:
        async def write_async(data):
            output.write(data)

        tasks = []
        for handle in handles:
            coro = tail_async(handle, interval, write_async)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.gather(*tasks)


# Example 10
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()

"""
The bottom-up approach:
(1)  Create a coroutine version of each leak funcitons.
(2)  Change synchronous functions so that the call the coroutine versions
and run the event loop.
(3)  Move up a level of the call hierarchy, make another layer of coroutines, and change call to
synchronous funcitons call to coroutines.
(4)  Delete synchoronous wrapperstines created in step 2 as you stop requiring them to glue
things together.
[EP, p, 287]

# Example 11
def tail_file(handle, interval, write_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def write_async(data):
        write_func(data)

    coro = tail_async(handle, interval, write_async)
    loop.run_until_complete(coro)


# Example 12
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()