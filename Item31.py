"""
Item 31:  Be Defensive When Iterating Over Arguments 

"""

import logging
from pprint import pprint

# Example 1: Given a list of numbers creates a list of the percentage of the total for each element.
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 2:  Show normalize in action.
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


# Example 3
path = 'my_numbers.txt'
with open(path, 'w') as f:
    for i in (15, 35, 80):
        f.write('%d\n' % i)

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


# Example 4:  The iterator it only produces its results once so the final list is empty.
it = read_visits('my_numbers.txt')
print(f'list(it) = {list(it)}')
percentages = normalize(it)
print(f'list(it) ={list(it)}')
print(percentages)


# Example 5
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it))  # The iterator is lready exhausted so this list is empty.


# Example 6:    We fix the problem with Example 3 by copy the the iterator to a list.
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 7
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


# Example 8
def normalize_func(get_iter):
    total = sum(get_iter())   # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 9:  To avoid copying the iterator's contaents we use a function that
# creates a new iterator each time.
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


# Example 10:  THe best solution is to use the iterator protocol by implementing the
# __iter__ method. 
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):  # 
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


# Example 11
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


# Example 12
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # An iterator -- bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits)  # No error

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


# Example 13
from collections.abc import Iterator 

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits)  # No error

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


# Example 14
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0


# Example 15:  Shows that the defensive approach only works with iterable containers.
try:
    visits = [15, 35, 80]
    it = iter(visits)
    normalize_defensive(it)
except:
    logging.exception('Expected')
else:
    assert False