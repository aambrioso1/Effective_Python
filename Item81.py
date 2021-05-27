"""
Item 81: Use tracemalloc to Understand Memory Usage and Leaks

Consists of four different programs:
(1) top_n.py
(2) using_gc.py
(3) waste_memory.py
(4) with_trace.py

It can be difficult to understand memory use and leaks in Python
The gc module can help you understand which objects exist but not how they are allocated.
The tracemalloc built-in module provides powerful tools for understanding sources memory usage.


"""

