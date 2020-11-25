# -*- coding: utf-8 -*-
"""
Item 3: Know the Difference between bytes and str

"""

a = b'h\x65llo'
print(list(a))
print(a)

a ='it is a\u0300 propos'
print(list(a))
print(a)

def to_str(bytes_or_str):
	if isinstance(bytes_or_str, bytes):
		value = bytes_or_str.decode('utf-8')
	else:
		value = bytes_or_str
	return value # Instance of str

print(repr(to_str(b'foo')))
print(repr(to_str('bar')))

def to_bytes(bytes_or_str):
	if isinstance(bytes_or_str,str):
		value = bytes_or_str.encode('utf-8')
	else:
		value = bytes_or_str
	return value # Instance of bytes

print(repr(to_bytes(b'foo')))
print(repr(to_bytes('bar')))

# You can add str and str as well as bytes and bytes.
# You can add str and bytes

# bytes contains sequences of 8-bit values, and str contains
# sequences of unicode patterns.
# If you want to read and write files use 'rb' and 'wb' respectively.

print(b'one' + b'two')
print('one' + 'two')

assert b'red' > b'blue'
assert 'red' > 'blue'

try:
	assert 'red' > b'blue'
except TypeError:
	print('Oops!  > not supported between bytes and str')


print(b'foo' == 'foo')

with open('data.bin', 'wb') as f:
	f.write(b'\xf1\xf2\xf3\xf4\xf5')

with open('data.bin', 'rb') as f:
	data = f.read()

assert data == b'\xf1\xf2\xf3\xf4\xf5'

with open('data.bin', 'r', encoding='cp1252') as f:
	data = f.read()

print(data)



