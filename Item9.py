"""
Item 8:  Use zip to Process Iterators in Parallel
"""

names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
longest_name = None
max_count = 0

for name, count in zip(names, counts):
	if count > max_count:
		longest_name = name
		max_count = count

print(f'The longest name is {longest_name}.')

names.append('Rosalind')

for name, count in zip(names, counts):
	print(name)


# Use zip_longest in itertools to avoid truncating if zip lists are of unequal size.
import itertools as it

for name, count in it.zip_longest(names, counts):
	print(f'{name}: {count}')
