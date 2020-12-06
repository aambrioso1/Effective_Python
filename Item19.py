"""
Item 19:  Never Unpack More Than Three Variables When Functions Return Multiple Values
"""


import logging
from pprint import pprint

# Example 1: Unpacking can be used to return multiple values from functions 
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths)  # Two return values

print(f'Min: {minimum}, Max: {maximum}')
#  Note that get_stats really returns a tuple.
print(f'get_stats(lengths) = {get_stats(lengths)}')

# Example 2:  Unpacking and returning multiple values work the same way.
first, second = 1, 2
assert first == 1
assert second == 2

def my_function():
    return 1, 2

first, second = my_function()
assert first == 1
assert second == 2


# Example 3:  Starred expressions and catch-all unpacking can be used with multiple-valued functions.
def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

longest, *middle, shortest = get_avg_ratio(lengths)

print(f'Longest:  {longest:>4.0%}')
print(f'Shortest: {shortest:>4.0%}')


# Example 4:  Returning too many values can be confusing and error prone.
# Avoid using more than three variables.
# If you need to unpack more return values use a class or a namedtuple (see Item 37).
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)

print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count {count}')

assert minimum == 60
assert maximum == 73
assert average == 67.5
assert median == 68.5
assert count == 10

# Verify odd count median
_, _, _, median, count = get_stats([1, 2, 3])
assert median == 2
assert count == 3


# Example 5
# Correct:
minimum, maximum, average, median, count = get_stats(lengths)

# Oops! Median and average swapped:
minimum, maximum, median, average, count = get_stats(lengths)


# Example 6
minimum, maximum, average, median, count = get_stats(
    lengths)

minimum, maximum, average, median, count = \
    get_stats(lengths)

(minimum, maximum, average,
 median, count) = get_stats(lengths)

(minimum, maximum, average, median, count
    ) = get_stats(lengths)
