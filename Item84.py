"""
Item 84: Write Docstrings for Every Function, Class, and Module

Write documentation for every module, class, method, and function using docstrings.
Keep them up-to_date.
For modules introduce the content and any important classes or functions.
For classes document behavior, important attributes, and subclass behavior.
For functions and methods document every weakness, returned value, raised exceptions,
and other behaviors.
For type annotations, omit providing information in the docstring that is already in the annotations.

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
def palindrome(word):
    """Return True if the given word is a palindrome."""
    return word == word[::-1]

assert palindrome('tacocat')
assert not palindrome('banana')


# Example 2
print(repr(palindrome.__doc__))


# Example 3
"""Library for finding linguistic patterns in words.
Testing how words relate to each other can be tricky sometimes!
This module provides easy ways to determine when words you've
found have special properties.
Available functions:
- palindrome: Determine if a word is a palindrome.
- check_anagram: Determine if two words are anagrams.
...
"""


# Example 4
class Player:
    """Represents a player of the game.
    Subclasses may override the 'tick' method to provide
    custom animations for the player's movement depending
    on their power level, etc.
    Public attributes:
    - power: Unused power-ups (float between 0 and 1).
    - coins: Coins found during the level (integer).
    """


# Example 5
import itertools
def find_anagrams(word, dictionary):
    """Find all anagrams for a word.
    This function only runs as fast as the test for
    membership in the 'dictionary' container.
    Args:
        word: String of the target word.
        dictionary: collections.abc.Container with all
            strings that are known to be actual words.
    Returns:
        List of anagrams that were found. Empty if
        none were found.
    """
    permutations = itertools.permutations(word, len(word))
    possible = (''.join(x) for x in permutations)
    found = {word for word in possible if word in dictionary}
    return list(found)
    

assert find_anagrams('pancakes', ['scanpeak']) == ['scanpeak']


# Example 6
# Check types in this file with: python -m mypy <path>
"""
from typing import Container, List

def find_anagrams(word: str,
                  dictionary: Container[str]) -> List[str]:
    pass
"""
# Example 7
# Check types in this file with: python -m mypy <path>



#from typing import Container, List

#def find_anagrams(word: str,
#                  dictionary: Container[str]) -> List[str]:
#    """Find all anagrams for a word.
#    This function only runs as fast as the test for
#    membership in the 'dictionary' container.
#    Args:
#        word: Target word.
#        dictionary: All known actual words.
#    Returns:
#        Anagrams that were found.
#    """
#    pass

