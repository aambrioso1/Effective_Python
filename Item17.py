"""
Item 17:  Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
"""

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
print(visits.data)


# Example 5: Setdefault has a confusing name and the code constructs a new set on every call.  
# A better way to implement this behavior is to use defaultdict in the collections built-in module.
from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)


print(TEST_DIR)