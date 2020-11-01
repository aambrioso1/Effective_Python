"""
Item 23:  Provide Optional Behaviors with Keyword Arguments

"""

def remainder(number, divisor):
	return number % divisor

# Can mix and match positional and keyword arguments but position arguments must come first.
print(f'Mix and match positional and keyword arguments remainder(20, divisor=7) = {remainder(20, divisor=7)}')

# Can use ** operator to pass dictionary values as corresponding keyword arguments
my_kwargs = {
	'number': 20,
	'divisor': 7,
}

print(f'Using a dictionary remainder(**my_kwargs) = {remainder(**my_kwargs)}')

def print_parameters(**kwargs):
	for key, value in kwargs.items():
		print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, gamma=4)

