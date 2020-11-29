"""
Item 11:  Know How to Slice Sequences

"""

a = [i for i in 'abcdefgh']
# Typical examples
# The form is a[start: end] with start being inclusive and end exclusive.
# Positive and negative integer indices are allowed.

print(f'a[:] is {a[:]}')          #
print(f'a[:5] is {a[:5]}')        #
print(f'a[:-1] is {a[:-1]}')      #
print(f'a[4:] is {a[4:]}')        #
print(f'a[-3:] is {a[-3:]}')      #
print(f'a[2:5] is {a[2:5]}')      #
print(f'a[2:-1] is {a[2:-1]}')    #
print(f'a[-3:-1] is {a[-3:-1]}')  #

# The result of a slice is a whole new list.

# When an assignment is made slice replace the specific range in the orginal list.

print('Before ', a)
a[2:7] = [99, 22, 14]
print('After a[2:7] = [99, 22, 14] ', a)

print('Before ', a)
a[2:3] = [47, 11]
print('After a[2:3] = [47, 11] ', a)

# Copy of the list
b = a[:]

"""
Things to remember
Leave out indices when you can.   Don't use 0 or len() for start or end.
Slicing is forgiving if start or end are out of range (assumes start or end).
Assigning to a list slice replace that range in te original seuqce with what's referenced
even if lengths are different.
"""