#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Works becuase dialog is loaded late and previous import is complete.
# This change does not follow the PEP 8 style guide because the import statement is not at the top.
# for the code.  Not a good solution since it small schanges in the code my
# break the module.

class Prefs:
    def get(self, name):
        pass

prefs = Prefs()

import dialog  # Moved
dialog.show()