"""
Item 30: Consider Generators Instead of Returning Lists

Generators can be clearer than list of results.
Generators can produce output for arbitrarily large input because their working memory
doesn't all inputs and outputs.
"""

address = "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."

# A generator is a functions that uses yield expressions instead of return expressions.
def index_words_iter(text):
	if text:
		yield 0
	for index, letter in enumerate(text):
		if letter == ' ':
			yield index + 1

# The next function can be used to generator successive results
it = index_words_iter(address)

print(next(it))
print(next(it))

# Output of a generator is iterable.
print(f'type(it) = {type(it)}') 
result = list(it)
print(result[:50])

def index_file(handle):
	offset = 0
	for line in handle:
		if line:
			yield offset
		for letter in line:
			offset += 1
			if letter == ' ':
				yield offset

import itertools

# With the generator, index_file(f), working memory is limited to maximum length of one line of input.
# We can also control how many value we want to generate.  
# Here we use islice from the itertools library to generate the desired values.  
# The itertools library has other tools for working with iterators and generators.
with open('C:\\Users\\Alex\\Effective_Python\\address.txt', 'r') as f:
	it = index_file(f)
	results = itertools.islice(it, 0 , 50)
	print(list(results))