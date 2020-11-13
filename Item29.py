"""
Item 29:  Avoid Repeated Work in Comprehensions by Using Assignment Expressions

"""

stock = {
	'nails':  125,
	'screws': 35,
	'wingnuts': 8,
	'washers': 24,
}

order = ['screws', 'wingnuts', 'clips']

def get_batches(count, size):
	return count // size

result = {}
for name in order:
	count = stock.get(name, 0)
	batches = get_batches(count, 8)
	if batches:
		result[name] = batches
print(f'result: {result}')

# Use a dictionary comprehension to shorten this code.
found = {name: get_batches(stock.get(name, 0), 8)
		for name in order
		if get_batches(stock.get(name, 0), 8)}
print(f'found: {found}')

# To avoid the repeated code above we can use the walrus operator.
# Note that the assignment is made in the condition since this is evaluated first.
# If the assignment is made in the value expression it will cause an NameError.
found_better = {name: batches for name in order
		if (batches := get_batches(stock.get(name, 0), 8))}
print(f'found_better: {found}')

# One other advantage of the comprehensions is that they avoid the leakage caused by looping.

# This example leaks because of the assignment operator.
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} is {last}')

# This example leaks.
for count in stock.values():
	pass
print(f'Last item of {list(stock.values())} is {count}')

# This example has a loop variable in a comprehension and does not leak.
half = [count_comp // 2 for count_comp in stock.values()]
print(f'half = {half}')

try:
	count_comp
except NameError:
	print('Oops!  name \'count_comp\' is not defined')

# An assignment expression also works with generator expressions
found = ((name, batches) for name in order
		if (batches := get_batches(stock.get(name, 0), 8)))
print(f'next(found): {next(found)}')
print(f'next(found): {next(found)}')
