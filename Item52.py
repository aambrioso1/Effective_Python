"""
Item 52:  Use subprocess to Manage Child Processes 

"""

"""
Child processes run in parallel
Use the run function for simple usage and Popen class for advance usage like UNIX-style pipelines
Use the timeout and communicate methods to avoid deadlocks or hanging processes.

Documentation for the subprocess module (Python 3.9.2):  https://docs.python.org/3/library/subprocess.html


run method convenience function

https://docs.python.org/3/library/subprocess.html#subprocess.run


Popen constructor
https://docs.python.org/3/library/subprocess.html#popen-constructor

"""


#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1:  Use the run convenience function for simple processes.
import subprocess
# Enable the next two lines to make this example work on Windows
import os
os.environ['COMSPEC'] = 'powershell'

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    # Enable this line to make this example work on Windows
    shell=True,
    encoding='utf-8')

result.check_returncode()  # No exception means it exited cleanly
print(result.stdout)


# Example 2:  Note the many adjustments for Windows.   
# Use this next line instead to make this example work on Windows

# We open a subprocess and continue on to something else while polling the subprocess to see if its done.
proc = subprocess.Popen(['sleep', '1'], shell=True)
# proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None: # Exit this loop when the subprocess terminates (proc.poll() == 0)
    print('Status', proc.poll())
    print('Working...')
    # Some time-consuming work here
    import time
    time.sleep(0.3)

print('Exit status', proc.poll())


# Example 3:   We "decouple"  the child processes by creating a list of processes (sleep_procs).
# In this example 10 child processes run in parallel.
import time

start = time.time()
sleep_procs = []
for _ in range(10):
    # Use this next line instead to make this example work on Windows
    proc = subprocess.Popen(['sleep', '1'], shell=True)
    # proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)


# Example 4
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'Parallel version finished in {delta:.3} seconds')


# Run the programs serially
start = time.time()

for _ in range(10):
    # Use this next line instead to make this example work on Windows
    proc = subprocess.Popen(['sleep', '1'], shell=True)
    proc.communicate()
    # proc = subprocess.Popen(['sleep', '1'])


end = time.time()
delta = end - start
print(f'Serial version finished in {delta:.3} seconds')


# Example 5:  We can pipe data froma Python program into a subprocess and retrieve its output.
#  This allows us to coordinate many other programs and work in parallel.
import os
# On Windows, after installing OpenSSL, you may need to
# alias it in your PowerShell path with a command like:
# $env:path = $env:path + ";C:\Program Files\OpenSSL-Win64\bin"
# $env:path = "C:\Program Files\OpenSSL-Win64\bin"

# This next line worked since openssl.exe is installed in this Git folder.
# Note that syntax is used since we need to keep the current paths.
# Also not that the change is temporary and will revert once active PowerShell is exited.
# $env:path = $env:path + ";C:\Program Files\Git\usr\bin\"

# A function to encrpyt some data using openssl.
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure that the child gets input
    return proc

# Example 6:  We use random bytes to encrypt three strings in parallel.
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)


# Example 7:  The communicate() method returns the encrypted data
for proc in procs:
    # out, _ = proc.communicate()
    out, second_item = proc.communicate()
    print(out[-10:], second_item)



# Example 8:  This is a very interesting example.   We couple the output of one child process to another to create chains
# of parallel processes.
"""
https://en.wikipedia.org/wiki/Whirlpool_(hash_function)

Whirlpool is a hash designed after the Square block cipher, and is considered to be in that family
of block cipher functions.  Whirlpool is a Miyaguchi-Preneel construction based on a substantially
modified Advanced Encryption Standard (AES).

https://en.wikipedia.org/wiki/Cryptographic_hash_function
A cryptographic hash function (CHF) is a mathematical algorithm that maps data of arbitrary size 
(often called the "message") to a bit array of a fixed size (the "hash value", "hash", or "message digest").
It is a one-way function, that is, a function which is practically infeasible to invert.
"""

def run_hash(input_stdin):  # Creates a Whirlpool hash of the input stream.
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)


# Example 9:  The first set of processes encrypt the data and the second hash the encrypted data.
encrypt_procs = [] # List of encrypting processes
hash_procs = [] # List of hashing processes
for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # Ensure that the child consumes the input stream and
    # the communicate() method doesn't inadvertently steal
    # input from the child. Also lets SIGPIPE propagate to
    # the upstream process if the downstream process dies.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None


# Example 10:  Note the the I/O between the child processes happens automatically.
for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])
    assert proc.returncode == 0


# Example 11:  The timeout parameter will raise an exception if a child process has not
# finished within the given time period.  The exception can be used to deal with the "misbehaving"
# child. 

# Use this next line instead to make this example work on Windows
proc = subprocess.Popen(['sleep', '10'], shell=True) # This process sleeps longer than the timeout so the 
# exemption is raised.
# proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status with exception', proc.poll())


proc = subprocess.Popen(['sleep', '1'], shell=True) # This process sleeps longer than the timeout so the 
# exemption is raised.
# proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=2)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status without exception', proc.poll())