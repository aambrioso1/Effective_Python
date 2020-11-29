"""
Item 9:  Avoid else Blocks after for and while Loops
"""

for i in range(3):
	print('Loop', i)
else:
	print('Else block!')


"""
The else after a block runs only if the loop body encounters a break statement.
Avoid them because their behavior is not intuitive.
"""