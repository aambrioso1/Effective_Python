#!/usr/bin/env PYTHONHASHSEED=1234 python3

# This is the function we wish to test.   See utils_test.py for the structure of the test.


def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('Must supply str or bytes, '
                        'found: %r' % data)