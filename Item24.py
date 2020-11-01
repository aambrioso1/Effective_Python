"""
Item 24:  Use None and Docstrings to Specify Dynamic Default Arugments

"""

from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
	print(f'{when}: {message}')

log('Hi there!')
sleep(0.1)
log("Hello again!")

