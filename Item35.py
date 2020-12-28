"""
Item 35: Avoid Causing State Transitions in Generators with throw

"""

import logging
from pprint import pprint


# Example 1:  Think of throw as meaning "throw an exception."  This example demonstrates how throw behaves.
try:
    class MyError(Exception):
        pass
    
    def my_generator():
        yield 1
        yield 2
        yield 3
    
    it = my_generator()
    print(next(it))  # Yield 1
    print(next(it))  # Yield 2
    print(it.throw(MyError('test error'))) # Third iteration will return "test error"
except:
    logging.exception('Expected')
else:
    assert False


# Example 2:  Shows how to inject an exception with a throw statement
def my_generator():
    yield 1

    try:
        yield 2
    except MyError:
        print('Got MyError!')
    else:
        yield 3

    yield 4

it = my_generator()
print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(it.throw(MyError('test error'))) # Exception thrown on third iteration


# Example 3:  Examples 3 and 4 demonstate how throw might be used.
# Throw is used to reset the time.
class Reset(Exception):
    pass

def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period


# Example 4
# This list is polled on each iteration to decide if a reset is needed
RESETS = [
    False, False, False, True, False, True, False,
    False, False, False, False, False, False, False] 

def check_for_reset():
    # Poll for external event
    return RESETS.pop(0)

def announce(remaining):
    print(f'{remaining} ticks remaining')

def run():
    it = timer(4)    
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)
print('Behavior using throw:')
run()


# Example 5:  Avoid using throw.  A better way to implement the behavior above is to define a class.  
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current

# Example 6
RESETS = [
    False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

print('\nBehavior using a class:')
run()