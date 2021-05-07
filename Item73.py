"""
Item 73:  Know How to Use heapq for Priority Queues 

Priority queues allow you to process items in order of importance.
List operations for priority queues will not scale well.
The heapq built in module provides all the functions you need to implement
a priority queue.
To use heapq the items to be prioritized must have an a natural search order.
This requires the __lt__ special method to be defined for classes.

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


# Example 1:  We create a book class to represent book titles and their due date
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


# Example 2:  We define a function to add books to a list and sort them by due date.
def add_book(queue, book):
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True) # Note the use of the sort command and a lambda function

# We set up a queue of overdue books.
queue = []
add_book(queue, Book('Don Quixote', '2019-06-07'))
add_book(queue, Book('Frankenstein', '2019-06-05'))
add_book(queue, Book('Les Misérables', '2019-06-08'))
add_book(queue, Book('War and Peace', '2019-06-03'))


# Example 3:  We create and exception for an empty queue and a function to retrieve the next overdue book given
# a queue of checked out books and a date.
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book

    raise NoOverdueBooks

# Example 4:  We pick due date and find the next two overdue books.
now = '2019-06-10'
before = '2019-6-6'

print('********** Next overdue_overdue_book start *************')
found = next_overdue_book(queue, now)
print(now, found.title)

found = next_overdue_book(queue, now)
print(now, found.title)

found = next_overdue_book(queue, before)
print(before, found.title)

found = next_overdue_book(queue, before)
print(before, found.title)
print('********** Next overdue_overdue_book complete *************')


# Example 5:  Remove books that are turn in on time from the queue
def return_book(queue, book):
    queue.remove(book)

# Now we can add books, return them, check if they are passed due, and know when they are all turn-in.
# The functions for checking and remove books will scale.   However, adding books books require that the list 
# be sorted again each time.   The time to do this will increase superlinearly.
queue = []
book = Book('Treasure Island', '2019-06-04')

add_book(queue, book)
print('Before return:', [x.title for x in queue])

return_book(queue, book)
print('After return: ', [x.title for x in queue])


# Example 6
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# Example 7:   We define a micro-benchmark to measure the performance of the list implementation.
import random
import timeit

print('******** Beginning of list_overdue_benchmark *********')

def print_results(count, tests):
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration

def print_delta(before, after):
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

def list_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            queue.append(i)
            queue.sort(reverse=True)

        while queue:
            queue.pop()

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# Example 8
baseline = list_overdue_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_overdue_benchmark(count)
    print_delta(baseline, comparison)
print('******** End of list_overdue_benchmark *********')
print('******** Beginning of list_return_benchmark *********')
# Example 9:  Now we benchmark the list_return.
def list_return_benchmark(count):
    def prepare():
        queue = list(range(count))
        random.shuffle(queue)

        to_return = list(range(count))
        random.shuffle(to_return)

        return queue, to_return

    def run(queue, to_return):
        for i in to_return:
            queue.remove(i)

    tests = timeit.repeat(
        setup='queue, to_return = prepare()',
        stmt=f'run(queue, to_return)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# Example 10:  
baseline = list_return_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_return_benchmark(count)
    print_delta(baseline, comparison)

print('******** End of list_return_benchmark *********')

# Example 11:  Now we use the built-in heapq module
from heapq import heappush

def add_book(queue, book):
    heappush(queue, book)


# Example 12:  This does not work because the Book class does not have a order defined.
try:
    queue = []
    add_book(queue, Book('Little Women', '2019-06-05'))
    add_book(queue, Book('The Time Machine', '2019-05-30'))
except:
    logging.exception('Expected')
else:
    assert False


# Example 13:   We add an ordering to the Book class by using the total_ordering decorator and implementing
# the __lt__ special method.
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date


# Example 14:  We create a queue of checked out books either using the add_book function or sort a pre-made list.
queue = []
add_book(queue, Book('Pride and Prejudice', '2019-06-01'))
add_book(queue, Book('The Time Machine', '2019-05-30'))
add_book(queue, Book('Crime and Punishment', '2019-06-06'))
add_book(queue, Book('Wuthering Heights', '2019-06-12'))
print([b.title for b in queue])


# Example 15
queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]
queue.sort()
print([b.title for b in queue])


# Example 16:  Or we can use the heapify function which will create a heap in linear time.  
#  Previous method will be complexity:  len(queue) * log(len(queue))
from heapq import heapify

queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]
heapify(queue)
print([b.title for b in queue])


# Example 17:  To check for overdue books we check the first element and use the heapq.heappop function.
from heapq import heappop

def next_overdue_book(queue, now):
    if queue:
        book = queue[0]           # Most overdue first
        if book.due_date < now:
            heappop(queue)        # Remove the overdue book
            return book

    raise NoOverdueBooks


# Example 18
now = '2019-06-02'

book = next_overdue_book(queue, now)
print(book.title)

book = next_overdue_book(queue, now)
print(book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# Example 19
def heap_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            heappush(queue, i)
        while queue:
            heappop(queue)

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)

print('******** heap overdue_book benchmark starts ***********')
# Example 20
baseline = heap_overdue_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = heap_overdue_benchmark(count)
    print_delta(baseline, comparison)
print('******** heap overdue_book benchmark ends ***********')

# Example 21
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False  # New field

    def __lt__(self, other):
        return self.due_date < other.due_date


# Example 22:  Now we create an efficient way to check if books have been turned in.   
# We leave books in the queue until their due date but check if they have been turned-in with the 
# next_overdue_book function.
def next_overdue_book(queue, now):
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue

        if book.due_date < now:
            heappop(queue)
            return book

        break

    raise NoOverdueBooks

queue = []

book = Book('Pride and Prejudice', '2019-06-01')
add_book(queue, book)

book = Book('The Time Machine', '2019-05-30')
add_book(queue, book)
book.returned = True

book = Book('Crime and Punishment', '2019-06-06')
add_book(queue, book)
book.returned = True

book = Book('Wuthering Heights', '2019-06-12')
add_book(queue, book)

now = '2019-06-11'

book = next_overdue_book(queue, now)
assert book.title == 'Pride and Prejudice'

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# Example 23
def return_book(queue, book):
    book.returned = True

print(f'{book.title=} and {book.due_date=} and {now=}')
print(f'{book.returned=}')
assert not book.returned
return_book(queue, book)
assert book.returned
print(f'{book.returned=}')
