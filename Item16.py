#!/usr/bin/env PYTHONHASHSEED=1234 python3

"""
Item 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys
"""

"""
"The three fundamental operations for interacting with dictionaries are 
accessing, assigning, and deleting keys and their associated values."
Four common ways to handle missing keys in dictionaries: using expressions,
KeyError exceptions, the get method, and the setdefault method.

The get method is best for dictionaries that contain basic types.

If the setdefault method seems like the bests fit consider using defaultdict instead.
See Item 17.
"""

import logging
from pprint import pprint

# Example 1
counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}


# Example 2:  Using a if statement to increment count even if key does not exist.
key = 'wheat'

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

print(counters)


# Example 3:  A better way to do the same thing by using the KeyError exception.
key = 'brioche'

try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

print(counters)


# Example 4:  The best way is to use get for dictionaries with simple types.
# Note that you for a dictionary of counters you should consider using the collections module.
key = 'multigrain'

count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


# Example 5:  Alternative code using KeyError approaches.
key = 'baguette'

if key not in counters:
    counters[key] = 0
counters[key] += 1

key = 'ciabatta'

if key in counters:
    counters[key] += 1
else:
    counters[key] = 1

key = 'ciabatta'

try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

print(counters)


# Example 6:  For more complex types.   Here each key item is associated with a list of votes.
# The in expression is used to decide if a key is new.
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}

key = 'brioche'
who = 'Elmer'

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []

names.append(who)
print(votes)


# Example 7:  Relying on the KeyError exception is an improvement over the in statement.
key = 'rye'
who = 'Felix'

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 8:  Use the get method to fetch a list values.
key = 'wheat'
who = 'Gertrude'

names = votes.get(key)
if names is None:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 9:  To improve readability and shorten the code use an assignment expression.
key = 'brioche'
who = 'Hugh'

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 10:  Using the setdefault method gives the same result.  It is shorter but less readable since 
# the purpose of setdefault is not clear from the name of the method.
key = 'cornbread'
who = 'Kirk'

names = votes.setdefault(key, [])
names.append(who)

print(votes)


# Example 11
data = {}
key = 'foo'
value = [] # Must assign a default value for each key which leads to "a significant performance overhead."
data.setdefault(key, value)
print('Before:', data)
value.append('hello')
print('After: ', data)


# Example 12:  You can use setdefault for the earlier counter example but this leads to an extra and unecessary
# assignment.
key = 'dutch crunch'

count = counters.setdefault(key, 0)
counters[key] = count + 1

print(counters)