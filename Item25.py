"""
Item 25:  Enforce Clarity with Keyword-Only and Positional-Only Arguments
Shows interesting new syntax in Python 3.8.   Arguments before / will be positional only.   Arguments after *
are keyword-only.   Arguments between * and / can be either.
Note that in Python functions positional arguments must come before keyword arguments.

"""

def safe_division(numerator, denominator, /, 
					ndigits=10, *, ignore_overflow=False,
					ignore_zero_division=False):
	try:
		fraction = numerator / denominator
		return round(fraction, ndigits)
	except OverflowError:
		if ignore_overflow:
			return 0
		else:
			raise
	except ZeroDivisionError:
		if ignore_zero_division:
			return float('inf')
		else:
			raise

result = safe_division(22,7)
print(result)

result = safe_division(22, 7, 5)
print(result)

# Note that the arguments between / and * can be set by position or keyword.
result = safe_division(22, 7, ndigits=2)
print(result)

#Returns division by zero exception
# result = safe_division(22,0)
# print(result)

# Error since denominator is a position-only argument (it occurs before the /)
# result = safe_division(22, denominator=7)
# print(result)

# Returns 0 since ignore_overflow=True
result = safe_division(22, 10**500, ignore_overflow=True)
print(result)

# Returns inf since ignore_zero_division+True
result = safe_division(22,0, ignore_zero_division=True )
print(result)

result = safe_division(22, 7, 5)
print(result)

result = safe_division(22, 7, ndigits=2)
print(result)

# Returns division by zero exception
# result = safe_division(22,0)
# print(result)

result = safe_division(22, 7, 5)
print(result)

result = safe_division(22, 10**500, ignore_overflow=True)
print(result)

# Returns an error since that last two arguments are keyword only.   They occur after the *
# result = safe_division(22, 7, 3, True, True)
# print(result)