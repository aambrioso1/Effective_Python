#!/usr/bin/env PYTHONHASHSEED=1234 python3

from analysis.utils import inspect
from frontend.utils import inspect  # Overwrites!
'frontend' in inspect.__module__
print(inspect.__module__)