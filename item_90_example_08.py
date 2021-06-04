#!/usr/bin/env PYTHONHASHSEED=1234 python3

# item_90_example_08.py

# Example 8
# Check types in this file with: python -m mypy <path>

class Counter:
    def __init__(self) -> None:
        self.value: int = 0  # Field / variable annotation

    def add(self, offset: int) -> None:
        value += offset      # Oops: forgot "self."

    def get(self) -> int:
        self.value           # Oops: forgot "return"

counter = Counter()
counter.add(5)
counter.add(3)
assert counter.get() == 8