"""
Item 7:  Prefer enumerate over range
"""

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']

for i, flavor in enumerate(flavor_list, 1):
	print(f'{i}: {flavor}')
