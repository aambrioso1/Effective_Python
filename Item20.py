"""
Item 20:  Prefer Raising Exceptions to Returning None
(EF, p. 80)

Division function that checks for division by zero and has type annotations.
"""


def careful_divide(a: float, b: float) -> float:
	"""Divides a by b.

	Raises:
		ValueError:  When the inputs cannot be divided.
	"""
	try:
		return a / b
	except ZeroDivisionError as e:
		raise ValueError('Invalid inputs')

print(careful_divide.__doc__)
print(f'1.0 / 3.0 = {careful_divide(1.0, 3.0)}')
print(f'1.0 / 3 = {careful_divide(1.0, 3)}')
careful_divide(1.0, 0.0)