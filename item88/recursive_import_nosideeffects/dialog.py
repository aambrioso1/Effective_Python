#!/usr/bin/env PYTHONHASHSEED=1234 python3

import app

class Dialog:
    def __init__(self):
        pass

save_dialog = Dialog()

def show():
    print('Showing the dialog!')

def configure():
    save_dialog.save_dir = app.prefs.get('save_dir')