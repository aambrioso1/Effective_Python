#!/usr/bin/env PYTHONHASHSEED=1234 python3

# db_connection.py
import prod_main # __main__

class TestingDatabase:
    pass

class RealDatabase:
    pass

if prod_main.TESTING: #__main__.TESTING:
    Database = TestingDatabase
else:
    Database = RealDatabase

print(f'{Database=}')