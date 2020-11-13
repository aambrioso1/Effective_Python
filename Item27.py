"""
Item 27:  Use Comprehensions instead of map and filter

"""

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # a = [i + 1 for i in range(10)]

# List comprehension
squares = [x**2 for x in a]
print(f'squares = {squares}')

# Using map to create the same list
alt = map(lambda x: x**2, a)

# Filtering with comprehension
even_squares = [x**2 for x in a if x % 2 == 0]
print(f'even_squares {even_squares}')

# Using map and filter to create the same list
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares==list(alt), 'The lists are not equal.'

# dictionary comprehension
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
print(f'even_squares_dict = {even_squares_dict}')

# Using map and filter to create the same dictionary
alt_dict = dict(map(lambda x: (x, x**2), filter(lambda x: x % 2 == 0, a)))
print(f'alt_dict = {alt_dict}')

# Set comprehension
three_cubed_set = {x**3 for x in a if x % 3 == 0 }
print(f'three_cubed_set = {three_cubed_set}')