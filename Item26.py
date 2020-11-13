"""
Item 26:  Define Function Decorators with functools.wraps

"""
# Decorators are syntax to allow one function to modify another function.
# The wraps function is a decorator that copies all the important
# metadata about a wrapped function its wrapper.
from functools import wraps
import pickle


def trace(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		result = func(*args, **kwargs)
		print(f'{func.__name__} ({args!r}), {kwargs!r}) '
			f'-> {result!r}')
		return result
	return wrapper


@trace
def fibonacci(n):
	"""Return the n-th Fibonacci number"""
	if n in (0,1):
		return n
	return (fibonacci(n - 2) + fibonacci(n - 1)) # Can trace the recursive function with a decorator
print(fibonacci) # Note wrapper hides function information
help(fibonacci) # The wraps wrapper copies all the important metadata to the outer function: help works
print(f'result of pickle.dumps(fibonacci):', pickle.dumps(fibonacci)) # Pickle works
