# item_90_example_04.py

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 4
# Check types in this file with: python -m mypy <path>

def concat(a: str, b: str) -> str:
    return a + b

concat('first', b'second')  # Oops: passed bytes value