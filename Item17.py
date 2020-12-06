"""
Item 17:  Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
"""

# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint


# Example 1:  A dictionary to keep track of cities visited
visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}


# Example 2:  Add item with setdefault or expressions
visits.setdefault('France', set()).add('Arles')  # Short

if (japan := visits.get('Japan')) is None:       # Long
    visits['Japan'] = japan = set()
japan.add('Kyoto')
original_print = print
print = pprint

print(visits)
print = original_print


# Example 3:  You can create a class and use setdefault that hides the complexity of the setdefault call
# and provides a nicer interface for the user.
class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)


# Example 4:  Shows off the nice interface.   
visits = Visits()
visits.add('Russia', 'Yekaterinburg') # Compare to the short version above
visits.add('Tanzania', 'Zanzibar') # Compare to the short version above
visits.add('Russia', 'Moscow')
visits.add('Russia', 'St. Petersburg')
print(visits.data)


# Example 5: The setdefault method has a confusing name and the code constructs a new set on every call.  
# A better way to implement the desire behavior with a dictionary is to use defaultdict from the collections built-in module.
from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
visits.add('Russia', 'Moscow')
visits.add('Russia', 'St. Petersburg')
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)
# defaultdict easily turn to a dictionary.
print(dict(visits.data))
# But defaultdict works just like a Python dictionary.
print(visits.data['Russia'])