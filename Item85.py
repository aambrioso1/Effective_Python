"""
Item 85: Use Packages to Organize Modules and Provide Stable APIs

Uses two folders:
(1) api_package
Another folder
(A) mypackage
(a) __init__.py
(b) models.py
(c) utils.py

(B) api_consumer.py
(C) main.py

(2) namespace_package
Uses two folders:
(A) analysis
(a) __init__.py
(b) utils.py

(B) frontend
(a) __init__.py
(b) utils.py
and the following files
(C) main.py
(D) main2.py
(E) main3.py
(F) main4.py

Packages are modules that contain modules.   They allow you to organize code
into separate name consoles, non-conflictin namespaces with unique absolute module name.
Simple Packages are defined by adding an __init__.py file to a directory that contains
other source files.
You can provide an API by listing its names in the __all__ special attributes.
You can hide the internal implementation of a package by using __init__.py or naming internal-only members
with a leading underscore. 

__all__ is probably no neccessary a single team on a single codebase.

"""
