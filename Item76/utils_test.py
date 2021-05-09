#!/usr/bin/env PYTHONHASHSEED=1234 python3

# We create tests for each behavior of utils.py's to_str function.

# To run the test: $ python utils_test.py
# To test one case: $ python utils_test.py UtilsTestCase.test_to_str_bytes


from unittest import TestCase, main
from utils import to_str

class UtilsTestCase(TestCase):
    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_failing(self):
        self.assertEqual('incorrect', to_str('hello'))

if __name__ == '__main__':
    main()