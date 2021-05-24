"""
Item 78:  Use Mock to Test Code with Complex Dependencies

A mock "lets you provide expected resonses for dependent functions, given a set of expected call."
A fake "provides most the the behavior ... but with a simpler implementation.""

The unittest.mock module provides a way to simulate the behavior of interfaces.   Mocks set up
dependencies for tests.

When testing mocks it is important to test the behavior of code being test and hwo the dependent functions 
were called by the code.

Keyword-only arguments and the unittest.mock.patch family can be used to inject mocks into the code be tested.

"""

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


# Example 1:  Write a function that queries a database for all animals of a certain species.
class DatabaseConnection:
    def __init__(self, host, port):
        pass

class DatabaseConnectionError(Exception):
    pass

def get_animals(database, species):
    # Query the Database
    raise DatabaseConnectionError('Not connected')
    # Return a list of (name, last_mealtime) tuples


# Example 2:  No database so the function fails.
try:
    database = DatabaseConnection('localhost', '4444')
    
    get_animals(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False


# Example 3:  We create a mock test by using the Mock class and specifying the function we are testing.
# This lets mock know how to simulate its behavior.

from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)
expected = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]
mock.return_value = expected

# Example 4:  mock will behave like a function so the following method call results in an error.
try:
    mock.does_not_exist
except:
    logging.exception('Expected')
else:
    assert False

# Example 5:  Now we can use the mock to test function behavior and the database parameter will make sure
# that database dependency work.
database = object()

print(20 * '*')
result = mock(database, 'Meerkat')
assert result == expected
print('Meerkat =', result == expected)

"""
# Test the mock with bad data
result = mock(database, 'Monkey')
assert result == expected
print('Monkey =', result == expected)
print(20 * '*')
"""

# Example 6:  To verify that input is correct we use the assert_called_once_with() method.
mock.assert_called_once_with(database, 'Meerkat')

# Example 7
try:
    mock.assert_called_once_with(database, 'Giraffe')
except:
    logging.exception('Expected')
else:
    assert False


# Example 8: If you don't care about individual parameters you can use the ANY constant
from unittest.mock import ANY

mock = Mock(spec=get_animals)
mock('database 1', 'Rabbit')
mock('database 2', 'Bison')
mock('database 3', 'Meerkat')

mock.assert_called_with(ANY, 'Meerkat')


# Example 9:  It is possible to mock exceptions with the side_effect method.
# Check help(unittest.mock.Mock) for all the options.
try:
    class MyError(Exception):
        pass
    
    mock = Mock(spec=get_animals)
    mock.side_effect = MyError('Whoops! Big problem')
    result = mock(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False


# Example 10:   Now we create a actual testing situation.
# We create a function to feed all of the animals in a zoo.
def get_food_period(database, species):
    # Query the Database
    pass
    # Return a time delta

def feed_animal(database, name, when):
    # Write to the Database
    pass

def do_rounds(database, species):
    now = datetime.datetime.utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# Example 11:  To get the do_rounds function to use the mock dependent functions you can
# inject vaules as keyword-only arguments.
def do_rounds(database, species, *,
              now_func=datetime.utcnow,
              food_func=get_food_period,
              animals_func=get_animals,
              feed_func=feed_animal):
    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


# Example 12:  Now create all the mock instances and set their expectations.
from datetime import timedelta

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]

feed_func = Mock(spec=feed_animal)


# Example 13:  Tehn we can pass the mocks into the do_rounds function.
result = do_rounds(
    database,
    'Meerkat',
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func)

assert result == 2


# Example 14:  Then verify that everything works.
from unittest.mock import call

food_func.assert_called_once_with(database, 'Meerkat')

animals_func.assert_called_once_with(database, 'Meerkat')

feed_func.assert_has_calls(
    [
        call(database, 'Spot', now_func.return_value),
        call(database, 'Fluffy', now_func.return_value),
    ],
    any_order=True)


# Example 15:   The keyword-only method works but is is verbose and requires changing
# every function you want to test.   The unittest.mock.patch family of functions
# make it easier.
# Here we override get_animals to be a mock using patch.
from unittest.mock import patch

print('Outside patch:', get_animals)

with patch('__main__.get_animals'):
    print('Inside patch: ', get_animals)

print('Outside again:', get_animals)


# Example 16:  Patch works for many objects and attributes. But it won't work for all objects.
# In this example we try it with the utc.now to show that it won't work.

try:
    fake_now = datetime(2019, 6, 5, 15, 45)
    
    with patch('datetime.datetime.utcnow'):
        datetime.utcnow.return_value = fake_now
except:
    logging.exception('Expected')
else:
    assert False


# Example 17:  To avoid his problem we use a help functions.
def get_do_rounds_time():
    return datetime.datetime.utcnow()

def do_rounds(database, species):
    now = get_do_rounds_time()

with patch('__main__.get_do_rounds_time'):
    pass


# Example 18:  We can also use a keyword argument fir datetime.uctcnow.mock and patch for other mocks.
# Default indicates that a standard Mock should be used each name.   Autospec insures that all the genrated mocks
# will adhere stick to their specifications (autospec=True)
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# Example 19: In example we use the keyword argument approach and the patch.multiple.
# The patch.multiple corresponds to the names in __main__ that need to be mocked.

from unittest.mock import DEFAULT

with patch.multiple('__main__',
                    autospec=True,
                    get_food_period=DEFAULT,
                    get_animals=DEFAULT,
                    feed_animal=DEFAULT):
    now_func = Mock(spec=datetime.utcnow)
    now_func.return_value = datetime(2019, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ('Spot', datetime(2019, 6, 5, 11, 15)),
        ('Fluffy', datetime(2019, 6, 5, 12, 30)),
        ('Jojo', datetime(2019, 6, 5, 12, 45))
    ]


# Example 20:  Now the test is ready to run.
    result = do_rounds(database, 'Meerkat', utcnow=now_func)
    assert result == 2
    print(f'{result=}')

    result2 = do_rounds(database, 'Jojo', utcnow=now_func)
    print(f'{result2=}', 'for Jojo')


    get_food_period.assert_called_once_with(database, 'Meerkat')
    get_animals.assert_called_once_with(database, 'Meerkat')
    feed_animal.assert_has_calls(
        [
            call(database, 'Spot', now_func.return_value),
            call(database, 'Fluffy', now_func.return_value),
        ],
        any_order=True)