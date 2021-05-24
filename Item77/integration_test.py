#!/usr/bin/env PYTHONHASHSEED=1234 python3

# 

from unittest import TestCase, main

def setUpModule():  # This function is called 1st.
    print('* Module setup')

def tearDownModule(): # This is called last.
    print('* Module clean-up')

class IntegrationTest(TestCase):
    def setUp(self): # This function is called second.
        print('* Test setup') # This function is third. Then again 6th.

    def tearDown(self): # This is fifth.   Again 7th.
        print('* Test clean-up')

    def test_end_to_end1(self):  # This is 4th.
        print('* Test 1')

    def test_end_to_end2(self):
        print('* Test 2')

if __name__ == '__main__':
    main()