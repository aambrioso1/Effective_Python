"""
Item 74:  Consider memoryview and bytearray for Zero-Copy Interactions with Bytes 

The memoryview type provides a zero-copy interface for the reading and writing
slices of objects that support Python's high performance buffer protocol. [EP, 351]
The bytearry type provides a mutable type that can be used for zero-copy data with functions like
socket.recv.from.  [EP, 351]
A memory view can wrap a bytearray allowing for received data to be spliced into an arbitray buffer
without copy costs.  [EP, 351]
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


# Example 1:  Set up code to model a request for a chunk of video data.
def timecode_to_index(video_id, timecode):
    return 1234
    # Returns the byte offset in the video data

def request_chunk(video_id, byte_offset, size):
    pass
    # Returns size bytes of video_id's data from the offset

video_id = ...
timecode = '01:09:14:28'
byte_offset = timecode_to_index(video_id, timecode)
size = 20 * 1024 * 1024
video_data = request_chunk(video_id, byte_offset, size)


# Example 2:  Now we model receiving the request and returning a 20 MB chunk for data.
class NullSocket:
    def __init__(self):
        self.handle = open(os.devnull, 'wb')

    def send(self, data):
        self.handle.write(data)

socket = ...             # socket connection to client
video_data = ...         # bytes containing data for video_id
byte_offset = ...        # Requested starting position
size = 20 * 1024 * 1024  # Requested chunk size
import os

socket = NullSocket()
video_data = 100 * os.urandom(1024 * 1024)
byte_offset = 1234

chunk = video_data[byte_offset:byte_offset + size]
socket.send(chunk)


# Example 3:  Now we run a micro-benchmark to measure the performance of this way of slicing
# byte instances to create chunks.    The result is slow.   The method will only allow
# about 200 clients requesting chuncks simultaneously.   With asynchio we should be able to
# handle tens of thousands of simultaneous connections.
import timeit

def run_test():
    chunk = video_data[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
print(f'********* End of First Implemenation ********')

# Example 4:  A better way to doe this is to use Python's built-in memoryview type
# which using CPython's high-performance buffer protocol.    This can bring enormous
# speed up for that needs to quickly process large amounts of memory.
data = b'shave and a haircut, two bits'
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print('Size:           ', chunk.nbytes)
print('Data in view:   ', chunk.tobytes())
print('Underlying data:', chunk.obj)


# Example 5:   We add memoryview slicing.   The benchmark show this is will be able to handle
# 2 x 10^6 clients. [EP, 349]
video_view = memoryview(video_data)

def run_test():
    chunk = video_view[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
print('*********** End of second implementation ************')

# Example 6:  Now we model sending live video back to the server.    We will need to store
# vidoe data in a cache. 
class FakeSocket:

    def recv(self, size):
        return video_view[byte_offset:byte_offset+size]

    def recv_into(self, buffer):
        source_data = video_view[byte_offset:byte_offset+size]
        buffer[:] = source_data

socket = ...        # socket connection to the client
video_cache = ...   # Cache of incoming video stream
byte_offset = ...   # Incoming buffer position
size = 1024 * 1024  # Incoming chunk size
socket = FakeSocket()
video_cache = video_data[:]
byte_offset = 1234

chunk = socket.recv(size)
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size:]
new_cache = b''.join([before, chunk, after])


# Example 7:  Now we put together a test of slicing and joining the video to add it to the cache.
def run_test():
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    new_cache = b''.join([before, chunk, after])

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
print('*********** End of third implementation ************')

# Example 8
try:
    my_bytes = b'hello'
    my_bytes[0] = b'\x79'
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
my_array = bytearray(b'hello')
my_array[0] = 0x79
print(my_array)


# Example 10
my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)


# Example 11
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)


# Example 12
def run_test():
    chunk = write_view[byte_offset:byte_offset + size]
    socket.recv_into(chunk)

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
print(f'********** End of last implementation ***************')

