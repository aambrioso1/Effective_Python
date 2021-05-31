#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Reenabling this will break things.
# import app

class Dialog:
    def __init__(self):
        pass

# Using this instead will break things
# save_dialog = Dialog(app.prefs.get('save_dir'))
save_dialog = Dialog()

def show():
    import app  # Dynamic import
    save_dialog.save_dir = app.prefs.get('save_dir')
    print('Showing the dialog!')