"""
Item 71:  Prefer deque for Producer-Consumer Queues

The list type can be used for FIFO queue for producer-consumer queue by using append to add
times and pop(0) to receive items.   This is not ideal becauses p(0) degrade superlinearly. 

The deque class from the collections built-in module takes constant time regardless of length
for append and popleft.   It is a better choice for queues if performance is important.
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

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 1:   We generate an toy email class for demonstrating a FIFO queue
class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


# Example 2:  A helper function that checks for emails.
def get_emails():
    yield Email('foo@example.com', 'bar@example.com', 'hello1')
    yield Email('baz@example.com', 'banana@example.com', 'hello2')
    yield None
    yield Email('meep@example.com', 'butter@example.com', 'hello3')
    yield Email('stuff@example.com', 'avocado@example.com', 'hello4')
    yield None
    yield Email('thingy@example.com', 'orange@example.com', 'hello5')
    yield Email('roger@example.com', 'bob@example.com', 'hello6')
    yield None
    yield Email('peanut@example.com', 'alice@example.com', 'hello7')
    yield None

EMAIL_IT = get_emails()

class NoEmailError(Exception):
    pass

def try_receive_email():
    # Returns an Email instance or raises NoEmailError
    try:
        email = next(EMAIL_IT)
    except StopIteration:
        email = None

    if not email:
        raise NoEmailError

    print(f'Produced email: {email.message}')
    return email


# Example 3:  A helper function that produces an email and places them on a queue for processing.
#  Here we use the append method on the queue list.
def produce_emails(queue):
    while True:
        try:
            email = try_receive_email()
        except NoEmailError:
            return
        else:
            queue.append(email)  # Producer


# Example 4:  A helper function that uses the emails in in the queue.
# We use the pop(0) method on the queue list.
def consume_one_email(queue):
    if not queue:
        return
    email = queue.pop(0)  # Consumer
    # Index the message for long-term archival
    print(f'Consumed email: {email.message}')


# Example 5:  The looping function here puts the pieces together.
# We break up the process so that email can be accepted quickly and processed at a consistent rate
# for more stable performance.
def loop(queue, keep_running):
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)

def make_test_end():
    count=list(range(10))

    def func():
        if count:
            count.pop()
            return True
        return False

    return func


def my_end_func():
    pass

my_end_func = make_test_end()
loop([], my_end_func)


# Example 6:  Now we use timeit to run some bench marks and check the performance of the list append method.
import timeit

def print_results(count, tests):
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration

def list_append_benchmark(count):
    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = []',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# Example 7:   Here we measure the append method
def print_delta(before, after):
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

n = 25
print(n*'*', 'The append benchmark (list method)', n*'*')
baseline = list_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_append_benchmark(count)
    print_delta(baseline, comparison)
print(2 * n * '*')

# Example 8:   Now we runs tests on the pop(0) method.
def list_pop_benchmark(count):
    def prepare():
        return list(range(count))

    def run(queue):
        while queue:
            queue.pop(0)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)

print(n*'*', 'The pop benchmark (list method)', n*'*')
# Example 9
baseline = list_pop_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_pop_benchmark(count)
    print_delta(baseline, comparison)
print(2 * n * '*')

# Example 10:   The collection built in module has the deque class (double-ended queue)
# that provides constant time opperations for inserting and removing items from it beginning
# and end.

# Note that we only need to change the pop(0) method to popleft since the append method has the same name
# for a deque object of the collections module.
import collections

def consume_one_email(queue):
    if not queue:
        return
    email = queue.popleft()  # Consumer
    # Process the email message
    print(f'Consumed email: {email.message}')

def my_end_func():
    pass

my_end_func = make_test_end()
EMAIL_IT = get_emails()
loop(collections.deque(), my_end_func)


# Example 11: We benchmark the append method and note that its performance is about the same as for the
# list method (roughly constant time)
def deque_append_benchmark(count):
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)
    return print_results(count, tests)

print(n*'*', 'The append benchmark (deque method)', n * '*')
baseline = deque_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = deque_append_benchmark(count)
    print_delta(baseline, comparison)
print(2 * n * '*')


# Example 12:  Finally we bench mark the deque popleft method and find that it grows linearly unlike
# the pop(0) list method which varies superlinearly.
def dequeue_popleft_benchmark(count):
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)

print(n*'*', 'The popleft benchmark (deque method)', n*'*')
baseline = dequeue_popleft_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = dequeue_popleft_benchmark(count)
    print_delta(baseline, comparison)
print(2 * n * '*')