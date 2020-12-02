"""
Item 4:  Prefer Interpolated F-Strings Over C-style Format Strings and str.format

Slatlin:  "The combination of expressiveness, terseness, and clarity provided by f-strings makes them
the best built-in option for Python programmers."

"""


pantry = [
	('avocados', 1.25),
	('bananas', 2.5),
	('cherries', 15),
]

key = 'my_var'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)

formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)

# Adjacent string concatenation can add clarity.

for i, (item, count) in enumerate(pantry):
	print(f'#{i+1}: '
		f'{item.title():<10s} = '
		f'{round(count)}')

# Python expressions can appear in format specifier options.

places = 3
number = 1.23456
print(f'My number is {number:.{places}f}')