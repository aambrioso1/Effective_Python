"""
Item 64:  Consider concurrent.futures for True Parallelism

We demo a serial, threaded, and parallel version of apply the gcd function here to a list of large integers.

The serial version does not yield any speed improvement because the GIL prevents Python from using
mutiple cores in parallel.

The threaded version is even slower because of the overhead for starting and communicating with a pool of threads.

The parallel version does speed up the computation.   It actually splits the processes with the machines cores.

The ProcessPoolExecuter class creates child processes using data serialized into binary on local sockets to 
run the child processes in parallel and then merges the results.

"This scheme is well-suited to certain types of isolated, high-leverage tasks." [EP, p. 296]

Recommendation
First try ThreadPoolExececutor
Then try ProcessPoolExecutor
Finally if these options are not working consider using the multiprocessing module directly.

Moving CPU bottlenecks to C-extension modules can be an effective way to improve performance.

The multiprocessing module provides tool that can help make Python computations parallel with minimal effort.

Avoid the advance parts of the multiprocess module until you have exhausted other options.

[EP, 297]

"""




#!/usr/bin/env PYTHONHASHSEED=1234 python3

def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i
    assert False, 'Not reachable'