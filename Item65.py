"""
Item 65: Take Advantage of Each Block in try/except/else/finally

The try/finally block:  Allows you to run cleanup code even if exceptions are raised in the try block
The else/block:  Allows you to minimize code in the try block and to distiguish success from the try/except block.
The else block can be used to excecute code after a succesful try block and before the finally block.

"""


#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1:  We use try finally to handle exceptions in the try block and the run clean up code in the finally block
def try_finally_example(filename):
    print('* Opening file')
    handle = open(filename, encoding='utf-8') # May raise OSError
    try:
        print('* Reading data')
        return handle.read()  # May raise UnicodeDecodeError
    finally:
        print('* Calling close()')
        handle.close()        # Always runs after try block


# Example 2:  Shows the exception in the try block caused by reading a bad byte.  This is an err
# we are anticipating that we will need to handle.
try:
    filename = 'random_data.txt'
    
    with open(filename, 'wb') as f:
        f.write(b'\xf1\xf2\xf3\xf4\xf5')  # Invalid utf-8
    
    data = try_finally_example(filename)
    # This should not be reached.
    import sys
    sys.exit(1)
except:
    logging.exception('Expected')
else:
    assert False


# Example 3:  This examples shows an error occuring before the try block in the function of Example 1.
# We put this error outside the try block so that the finally block is not executed (handle.close)
try:
    try_finally_example('does_not_exist.txt')
except:
    logging.exception('Expected')
else:
    assert False

print('\n********** End of try/finally block **********\n')

# Example 4:  Now we include an else block to separate code from the try/except block.   
# In this example ValueError is handle by the try/except block and a KeyError is separated out by
# put this code in the else block.

import json

def load_json_key(data, key):
    try:
        print('* Loading JSON data')
        result_dict = json.loads(data)  # May raise ValueError
    except ValueError as e:
        print('* Handling ValueError')
        raise KeyError(key) from e
    else:
        print('* Looking up key')
        return result_dict[key]         # May raise KeyError


# Example 5:   The successful case key is looked up in the else block.
assert load_json_key('{"foo": "bar"}', 'foo') == 'bar'


# Example 6:  Input data is bad so the exception in caught in the except block
try:
    load_json_key('{"foo": bad payload', 'foo')
except:
    logging.exception('Expected')
else:
    assert False


# Example 7:  SInce the key lookup occurs in the the except block an exception is distinguished.
try:
    load_json_key('{"foo": "bar"}', 'does not exist')
except:
    logging.exception('Expected')
else:
    assert False


# Example 8:   This example puts it all together with a try/except/else/finally
"""
try block:  file the file process the except block
except block:  handle exception in the try block that are excepted
else block:  update the file in palnce and allow related exception to propogate up
finally block:  cleans up the file handle.  this block always runs
"""
print('**************** Example 8 starts *******************\n')

UNDEFINED = object()
DIE_IN_ELSE_BLOCK = False

def divide_json(path):
    print('* Opening file')
    handle = open(path, 'r+')   # May raise OSError
    try:
        print('* Reading data')
        data = handle.read()    # May raise UnicodeDecodeError
        print('* Loading JSON data')
        op = json.loads(data)   # May raise ValueError
        print('* Performing calculation')
        value = (
            op['numerator'] /
            op['denominator'])  # May raise ZeroDivisionError
    except ZeroDivisionError as e:
        print('* Handling ZeroDivisionError')
        return UNDEFINED
    else:
        print('* Writing calculation')
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)          # May raise OSError
        if DIE_IN_ELSE_BLOCK:
            import errno
            import os
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
        handle.write(result)    # May raise OSError
        return value
    finally:
        print('* Calling close()')
        handle.close()          # Always runs


# Example 9
print('**************** Everything works: try, else, and finally excecute *******************')

temp_path = 'random_data.json'

with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1

print('\n**************** The calulation is invalid (division by zero error) : try, except, and finally excecute *******************')
# Example 10
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED


# Example 11
print('\n**************** The jason data is bad: try and finally excecute *******************')
try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1 bad data')
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False


# Example 12:  New exception is raise and we know exception will be in the else block and clean up with the finally block.
print('\n**************** New exception raised: try, else, and finally excecute *******************')

try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1, "denominator": 10}')
    DIE_IN_ELSE_BLOCK = True
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False
