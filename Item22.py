"""
Item 22:  Reduce Visual Noise with Variable Positional Arguments

"""
# Functions can accept a variable number of positional arugments with *args.
def log(message, *values):
	if not values:
		print(message)
	else:
		values_str = ', '.join(str(x) for x in values)
		print(f'{message} {values_str}')

log('My numbers are', 1, 2)
log("Hi there!")

# You can use the items from a sequence (including a generator) as the position arguments of a function
# with the * operator.
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

def my_generator():
	for i in range(10):
		yield i

def my_func(*args):
	print(args)

it = my_generator()
my_func(*it)