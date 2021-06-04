# item_90_example_14.py

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 14
# Check types in this file with: python -m mypy <path>

class FirstClass:
    def __init__(self, value: SecondClass) -> None:
        self.value = value

class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value

second = SecondClass(5)
first = FirstClass(second)