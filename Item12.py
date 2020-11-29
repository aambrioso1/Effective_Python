"""
Item 12:  Avoid Striding and SLicing in a Single Expression

"""

x = ['red', 'orange', 'yellow', 'blue', 'green', 'purple']

print(f'odds = x[::2]', x[::2])
print(f'evens = x[1::2]', x[1::2])

# Reversing a string works with byte strings
x = 'Ambrioso'
y = x[::-1]
print(f'{x} reversed is {y}')

# And unicode
x = 'a\u0300 propos'
y = x[::-1]
print('x = ', x)
print('y = ', y)

# Breaks down when Unicode data is encoded in a UTF-8 byte string
w = 'Alex'
x = w.encode('utf-8')
y = x[::-1]
z = y.decode('utf-8')
print(f'w = {w}\nx = {x}\ny = {y}\nz = {z}')

# Striding can be confusing.  Avoid using it along with start and end values.
# If you must use a stride, avoid using start and end indices and use a positive stride.
# If you must x[] start and end indices, consider using one assignment for striding and one for slicing.
# This will make your intentions more clear.

x = 'abcdefgh'
y = x[::2]
z = y[1:-1]
print(f'x = {x}\ny = {y}\nz = {z}')