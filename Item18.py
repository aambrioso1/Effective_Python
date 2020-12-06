"""
Item 18:  Know How to Construct Key-Dependent Default Values with __missing__
"""

import logging
from pprint import pprint

# Example 1
pictures = {}
path = 'images/workstation.png'

with open(path, 'wb') as f:
    f.write(b'image data here 1234')

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(f'Example 1: pictures = {pictures}')
print(f'Example 1: image_data ={image_data}')


# Example 2
# Examples using in and KeyError
pictures = {}
path = 'profile_9991.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')

if path in pictures:
    handle = pictures[path]
else:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

pictures = {}
path = 'profile_9922.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')

try:
    handle = pictures[path]
except KeyError:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)


# Example 3
pictures = {}
path = 'profile_9239.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9239')

try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()

print(f'Example 3: pictures = {pictures}')
print(f'Example 3: image_data = {image_data}')


# Example 4
try:
    path = 'profile_4555.csv'
    
    with open(path, 'wb') as f:
        f.write(b'image data here 9239')
    
    from collections import defaultdict
    
    def open_picture(profile_path):
        try:
            return open(profile_path, 'a+b')
        except OSError:
            print(f'Failed to open path {profile_path}')
            raise
    
    pictures = defaultdict(open_picture)
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
path = 'account_9090.csv'

with open(path, 'wb') as f:
    f.write(b'image data here 9090')

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
print(f'Example 5: pictures = {pictures}')
print(f'Example 5: image_data = {image_data}')
