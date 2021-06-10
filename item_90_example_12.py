#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Example 12:
# Check types in this file with: python -m mypy <path>

from typing import Optional

def get_or_default(value: Optional[int],
                   default: int) -> int: 
    if value is not None:
        return value
    return value  # Oops: should have returned "default"