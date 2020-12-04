#!/usr/bin/env PYTHONHASHSEED=1234 python3

"""
Item 15: Be Cautious When Relying on dict Insertion Ordering

Effective Python:  https://effectivepython.com/

GitHub Code:  https://github.com/bslatkin/effectivepython/tree/master/example_code

"""

# Reproduce book environment
import random
# random.seed(1234)

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

# Example 1:  In Python 3.5 and before, iterating over a dict returned keys in an arbitrary order.


# Example 2:  Works as expected for Python 3.6 and above.

baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}
print(baby_names)

# Exanple 3:  Also with Python 3.5 and before dict methods like keys() and items() excepted random-like behavior


# Example 4: Works as expected for Python 3.6 and above. 
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem())  # Last item inserted

# Example 5: Also with Python 3.5 and before keyword arguments to functions would show random behavior


# Example 6:  Works as expected for Python 3.6 and above.
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')


# Example 8
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')

#  Note collections has an OrderedDict class with this similar good behavior with regard to order.
#  It has better performance for high-rate key insertions and popitem calls.

# Example 9
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}


# Example 10
def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


# Example 11
def get_winner(ranks):
    return next(iter(ranks))


# Example 12
ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)


# Example 13
from collections.abc import MutableMapping

class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)

my_dict = SortedDict()
my_dict['otter'] = 1
my_dict['cheeta'] = 2
my_dict['anteater'] = 3
my_dict['deer'] = 4

assert my_dict['otter'] == 1

assert 'cheeta' in my_dict
del my_dict['cheeta']
assert 'cheeta' not in my_dict

expected = [('anteater', 3), ('deer', 4), ('otter', 1)]
assert list(my_dict.items()) == expected

assert not isinstance(my_dict, dict)


# Example 14:  This does not work as expected because SortDict uses MutableMapping
# from the collections.abc built-in module.   The values are sorted alphabettically.

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)


# Example 15:  The best solution to the problem is to reimplement get_winner to return the item
# ranked 1.
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name

winner = get_winner(sorted_ranks)
print(winner)


# Example 16:  Another ideas it to check the type of ranks to make sure it matches expectations.
try:
    def get_winner(ranks):
        if not isinstance(ranks, dict):
            raise TypeError('must provide a dict instance')
        return next(iter(ranks))
    
    assert get_winner(ranks) == 'otter'
    
    get_winner(sorted_ranks)
except:
    logging.exception('Expected')
else:
    assert False

# Example 17
"""
Check types in this file with: python -m mypy <path>
Add type annotations to your Python programs, and use mypy to type check them. 
Mypy is essentially a Python linter on steroids, and it can catch many 
programming errors by analyzing your program, without actually having to run it.
Mypy has a powerful type system with features such as type inference, 
gradual typing, generics and union types.

pip install mypy

"""

from typing import Dict, MutableMapping

def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))

from typing import Iterator, MutableMapping

class SortedDict(MutableMapping[str, int]):
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self.data[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator[str]:
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self) -> int:
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(f'winner = {winner}')