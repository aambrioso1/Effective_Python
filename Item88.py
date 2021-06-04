"""
Item 88:  Know How to Break Circular Dependencies 

Uses four folders with:
(1)  recursive_import_bad
  (a) app.py
  (b) dialog.py
  (c) main.py
(2)  recursive_import_dynamic
  (a) app.py
  (b) dialog.py
  (c) main.py
(3)  recursive_import_nosideeffects
  (a) app.py
  (b) dialog.py
  (c) main.py
(4)  recursive_import_ordering
  (a) app.py
  (b) dialog.py
  (c) main.py


What Python does when a module is imported.
Depth-first search

1.  Searches sys.path
2.  Load modules and ensures it compiles.
3.  Creates a corresponding empty module.
4.  Inserts module into sys.modules.
5.  Runs the in the module to define its content.

Second import call for module may load before this process is completing by the first import call.   

First way to break dependencies:  refactor code so that process is complete before second call.
Second way reorder imports.
Third way is to import, configure, and run.  We only run configure once all the module have benn imported.
This works well and allows dependency injection.

Circular dependencies are a result of two modules must call each other at import time.
The best way to break them is by refactoring mutual dependencies in a separate module at the bottom
of the dependency tree.
Dyanamic imports are the simplest solutions but can degrade performance.

"""

