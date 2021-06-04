# item_90_example_02.py

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 2
# Check types in this file with: python -m mypy <path>

def subtract(a: int, b: int) -> int:  # Function annotation
    return a - b

subtract(10, '5')  # Oops: passed string value