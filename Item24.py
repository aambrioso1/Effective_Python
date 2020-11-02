"""
Item 24:  Use None and Docstrings to Specify Dynamic Default Arugments

"""

# Convention for insuring that default keyword is set to properly value AND function calls reevaluate
# the value.
from time import sleep
from datetime import datetime

def log(message, when=None):
	"""Log a message with a timestamp.
	
	Args:
		message:  Message to print.
		when: datetime of when message occured.
			Defaults to the present time.
		
	"""
	if when is None:
		when = datetime.now()
	print(f'{when}: {message}')

log('Hi there!')
sleep(0.1)
log("Hello again!")

# Mutable objects can have the same problem.   This can be resolved in the same way:  set the default
# to None and documents the functions behavior in the it's docstring.
import json

def decode(data, default=None):
	"""Load JSON dats from a string.

	Args:
		data: JSON data to decode
		default:  Value to return if decoding fails.
			Defaults to an empty dictionary.
	"""
	try:
		return json.loads(data)
	except ValueError:
		if default is None:
			default = {}
		return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo', foo)
print('Bar', bar)
assert foo is not bar

# The same approach works with type annotations.

from typing import Optional

def log_typed(message: str, 
				when: Optional[datetime]=None) -> None:

	"""Log a message with a timestamp

	Args:
		message:  Message to print.
		when:  datetime of when the message occurred.
			Defauls to the present time.
	"""
	if when is None:
		when = datetime.now()
	print(f'{when}: {message}')


log_typed('Hi there!')
sleep(0.1)
log_typed("Hello again!")


