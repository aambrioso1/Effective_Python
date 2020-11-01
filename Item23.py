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

#  Keyword arguments make purpose of arguments clearer

#  Keyword arguments can be used to add new behaviors to a function will remaining backward capatible
weight_diff = 0.5
time_diff = 3

# Extend function for longer time scales
def flow_rate(weight_diff, time_diff, period=1):
	return (weight_diff / time_diff) * period

print(f'flow per second: {flow_rate(weight_diff, time_diff):.3}')
print(f'flow per hour: {flow_rate(weight_diff, time_diff, period=3600)}')

#  Extend the function for other weight units

def flow_rate(weight_diff, time_diff, period=1, units_per_kg=1):
	return ((weight_diff * units_per_kg)/ time_diff) * period

print(f'pounds per hour: {flow_rate(weight_diff, time_diff, period=3600, units_per_kg=2.2)}')