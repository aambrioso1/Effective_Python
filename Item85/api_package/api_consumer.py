#!/usr/bin/env PYTHONHASHSEED=1234 python3

from mypackage import *

a = Projectile(1.5, 3)
b = Projectile(4, 1.7)
after_a, after_b = simulate_collision(a, b)
print(after_a.__dict__, after_b.__dict__)

import mypackage
try:
    mypackage._dot_product
    assert False
except AttributeError:
    pass  # Expected

mypackage.utils._dot_product  # But this is defined