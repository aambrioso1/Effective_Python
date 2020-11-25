"""
Item 5:  Write Helper Functions Instead of Complex Expressions
"""

from urllib.parse import parse_qs


my_values = parse_qs('red=5&blue=0&green=',
					keep_blank_values=True)

print(repr(my_values))

# Use a helper function.

def get_first_int(values, key, default=0):
	found = values.get(key, [''])
	if found[0]:
		return int(found[0])
	return default

green = get_first_int(my_values, 'green')