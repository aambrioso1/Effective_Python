"""
Item 63:  Avoid Blocking the asyncio Event Loop to Maximize Responsiveness

Since open, close, and write calls for output file handles happen in the main event loop,
these calls to the host operating system may block the event loop for significant amounts of time. 
This can slow down the code.

Making system calls in coroutines can slow down code.

The debug=True parameter of asyncio.run will help detect when coroutines are slowing the event loop down.


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


# Example 1
import asyncio

# On Windows, a ProactorEventLoop can't be created within
# threads because it tries to register signal handlers. This
# is a work-around to always use the SelectorEventLoop policy
# instead. See: https://bugs.python.org/issue33792
policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

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


# Example 2:  THis example shows how to use the debug=True parameter of the asynchio.run
# to identify the file and line of a bad cooroutine blocked by a slow system call

import time

async def slow_coroutine():
    time.sleep(0.5)  # Simulating slow I/O

asyncio.run(slow_coroutine(), debug=True)

print(10*'*', 'End of first example', 10*'*')

# Example 3:  To increase responsiveness the problemetic calls are call inside their own
# event loop using a new Thread subclass.

from threading import Thread

class WriteThread(Thread):
    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        self.output = None
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        with open(self.output_path, 'wb') as self.output:
            self.loop.run_forever()

        # Run one final round of callbacks so the await on
        # stop() in another event loop will be resolved.
        self.loop.run_until_complete(asyncio.sleep(0))


# Example 4:  Other threads can call and await in the above thread without a Lock.
    async def real_write(self, data):
        self.output.write(data)

    async def write(self, data):
        coro = self.real_write(data)
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop)
        await asyncio.wrap_future(future)


# Example 5:  Other coroutines can stop the worker thread in a threadsafe manner with similar code.
    async def real_stop(self):
        self.loop.stop()

    async def stop(self):
        coro = self.real_stop()
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop)
        await asyncio.wrap_future(future)


# Example 6:  This code allows the methods to be used with statements.
    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.start)
        return self

    async def __aexit__(self, *_):
        await self.stop()


# Example 7:  Now run_tasks can be refactored into a full asynchronous version that is 
# easy to read and avoids running slow system calls in the main thread.
class NoNewData(Exception):
    pass

def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()

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

async def run_fully_async(handles, interval, output_path):
    async with WriteThread(output_path) as output:
        tasks = []
        for handle in handles:
            coro = tail_async(handle, interval, output.write)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.gather(*tasks)


# Example 8
# This is all code to simulate the writers to the handles
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


# Example 9
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
        assert expected_lines == found_lines

input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_fully_async(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


print(10*'*', 'Got the the end', 10*'*')