"""
Item 32: Consider Generator Expressions for Large List Comrehensions

Based on: https://github.com/bslatkin/effectivepython/blob/master/example_code/item_32.py

"""

# Example 1
# This approach creates a list with every value.  
# Can be problematic if the number of values is large or infinite.
import random

# Creates a files to use for examples
with open('my_file.txt', 'w') as f:
    for _ in range(10):
        f.write('a' * random.randint(0, 100))
        f.write('\n')

# Use a list comprehension to create a list of the length of the strings in my_file.txt.
value = [len(x) for x in open('my_file.txt')]
print(f'values in my_file.txt: {value}')

"""
Example 2
The solution to this problem is generator expressions.   A generator expression
is a generalization of list comprehensions and generators.   You can create a generator expression by
using the same syntax used for list or set comprehension between ().
"""

#  Now it is a generator.   This allows the user to control how many values are generated.
it = (len(x) for x in open('my_file.txt'))
print(it)

"""
Example 3 and 3.5
Example 3
You can generate as many values as you like.
Example 3.5
This is my example.  If you need to use a generator several times you can use 
intertools.tee(iterable,n=2) which returns n independent iterables for a single iterable.  
See: https://docs.python.org/3/library/itertools.html#itertools.tee
There is much useful info in the docs on tee.  For example:  leave the original iterable alone, 
tee iterators are not threadsafe, and if one iterator uses most of its data before another starts, 
it is faster to use list() instead of tee().
"""

from itertools import tee
it1, it2 = tee(it) # Note the default is to return 2 independent iterables.
print(f'first it1 = {next(it1)}')
print(f'second it1 = {next(it1)}')


# Example 4:  We create a new generator that depends on it1.
roots1 = ((x, x**0.5) for x in it1)


# Example 5:  Shows the interdependence of it1 and roots1.
print(f'first roots1 = {next(roots1)}')
print(f'second roots1 = {next(roots1)}')
print(f'next(it1) = {next(it1)}')


# Example 6:  Shows that the two iterators, it1 and it2, as well is their dependents are independent of each other
# but their dependents are tied to the original generator.

roots2 = ((x, x**0.5) for x in it2)
print(f'First call roots2: {next(roots2)}')
print(f'Call next(it2) = {next(it2)}')
print(f'Second call roots2 = {next(roots2)}')