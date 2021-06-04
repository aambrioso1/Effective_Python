#!/usr/bin/env PYTHONHASHSEED=1234 python3

from analysis.utils import log_base2_bucket
from frontend.utils import stringify

bucket = stringify(log_base2_bucket(33))
print(repr(bucket))