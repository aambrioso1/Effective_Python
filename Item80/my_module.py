#!/usr/bin/env PYTHONHASHSEED=1234 python3
"""
You can initiate the Python interactive debugger by placing the built-in
breakpoint() function in your code.
The debugger is a full shell that lets you inspect the code.
The pdb shell commands allow you to control program execution precisely so you can
inspect the code.
You can even inspect programs that have crashed with the command:
python -m pdb -c continue <program path> or using the built-in REPL and the command:
import pdb; pdb.pm()

Some pdb commands:

p <variable name>
where
up
down
step
next
return
continue
quit

"""
import math

def squared_error(point, mean):
    err = point - mean
    return err ** 2

def compute_variance(data):
    mean = sum(data) / len(data)
    err_2_sum = sum(squared_error(x, mean) for x in data)
    variance = err_2_sum / (len(data) - 1)
    return variance

def compute_stddev(data):
    variance = compute_variance(data)
    return math.sqrt(variance)