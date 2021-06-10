# item_90_example_17.py

#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 17:  Code that will catch the error that was previous hidden in example 14.
from __future__ import annotations

class FirstClass:
    def __init__(self, value: SecondClass) -> None:  # OK
        self.value = value

class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value

second = SecondClass(5)
first = FirstClass(second)