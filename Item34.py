"""
Item 34: Avoid Injecting Data into Generators with send
It is better to provide an input iterator to a set of composed generators.
"""

import logging
from pprint import pprint


# Example 1:  A generator that generates values for a sine wave
import math

def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


# Example 2
def transmit(output):
    if output is None:
        print(f'Output is None')
    else:
        print(f'Output: {output:>5.1f}')

def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))


# Example 3: 
def my_generator():
    received = yield 1
    print(f'received = {received}')

it = my_generator()
output = next(it)       # Get first generator output
print(f'output = {output}')

try:
    next(it)            # Run generator until it exits
except StopIteration:
    pass
else:
    assert False


# Example 4
it = my_generator()
output = it.send(None)  # Get first generator output
print(f'output = {output}')

try:
    it.send('hello!')   # Send value into the generator
except StopIteration:
    pass
else:
    assert False


# Example 5
def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield             # Receive initial amplitude
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output # Receive next amplitude


# Example 6:  Send the item 
def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)

print(f'\nRun modulating')
run_modulating(wave_modulating(12))

# Example 7:  Multiple signals in sequence works when amplitude is fixed.

def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)

print(f'\nComplex wave')
run(complex_wave())

# Example 8:  Does not work here because each nested generator starts with a None.
def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)

print(f'\nRun modulating and complex')
run_modulating(complex_wave_modulating())


# Example 9:  Easiest solution is to pass an iterator into the wave function.
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)  # Get next input
        output = amplitude * fraction
        yield output


# Example 10:  Pass the same iterator.   Each nested iterator will start where the
# the previous one left off.   The iterators are said to be stateful [EP, p. 132]
def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


# Example 11:  Iterators can come from anywhere and could be dynamic.  But not thread safe.
def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)

run_cascading()