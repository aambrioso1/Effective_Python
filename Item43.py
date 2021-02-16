"""
Item 43: Inherit from collections.abc for Custom Container Types

The built-in collections.abc module provides a custom class with the typical methods used by Python container types (lists, sets, tuples, and dictionaries)

To obtain all the usual methods both __getitem__ and __len__ must be implemented.
See:  https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence

Many other abstract base classes can be implemented.
See:  https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes


"""
# Reproduce book environment
import random
random.seed(1234)

import logging # Used for exception handling
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
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):

        """builds a dictionary of the frequency of each item in a list."""

        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts


# Example 2:  By subclassing list we get all the list's standard functionality
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
help(FrequencyList.frequency)
print(f'foo.frequency {foo.frequency.__doc__}')
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())


# Example 3
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Example 4
bar = [1, 2, 3]
bar[0]


# Example 5
bar.__getitem__(0)


# Example 6:  To get a custom class to behave like a sequence you can implement the __getitem__ dunder method
class IndexableNode(BinaryNode):  # Traverses tree depth first
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')


# Example 7
tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))


# Example 8:   Sequence indexings is available and the in operator works.
print(tree)
print('LRR is', tree.left.right.right.value)
print('Index 0 is', tree[0])
print('Index 1 is', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))

try:
    tree[100]
except IndexError:
    pass
else:
    assert False


# Example 9:  Note that other list semantics are unavailable.   Here len does not work.
try:
    len(tree)
except:
    logging.exception('Expected')
else:
    assert False


# Example 10: One solution is to simply implement the dunder method for the functionality you want.
class SequenceNode(IndexableNode):
    def __len__(self):  # We implement __len__ for our tree.
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count


# Example 11
tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)

print('Tree length is', len(tree))


# Example 12
try:
    # Make sure that this doesn't work
    tree.count(4)
except:
    logging.exception('Expected')
else:
    assert False


# Example 13:  By inheriting from Sequence in the collections.abc build in module and implemented
# the right dunder methods all the other methods will be provided.
try:
    from collections.abc import Sequence
    
    class BadType(Sequence):
        pass
    
    foo = BadType()
except:
    logging.exception('Expected')
else:
    assert False


# Example 14:
class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right=BetterNode(
        15,
        left=BetterNode(11))
)

# Now we get the index and count methods for free.
print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))

"""
Note that for more complex container types like Set and MutableMapping there are a large
number of special method that need to be implemented to match Python conventions.  

These ideas go beyond the collections.abc module.   Python uses a variety of special methods for 
comparisons and sorting.
"""
