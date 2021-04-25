"""
Item 61: Know How to Port Threaded I/O to asyncio

This item shows how to port code that does threaded, blocking I/O over coroutines and asynchronous I/O.

Slaitkin implements a TCP-based server (Transfer Control Protocol.  See https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
for guessing a number.   This type of client/server is typically built using blocking I/O and threads.


Python provides asynchronous versions of for loops, with statements, generators, comprehensions, and library
helper functions.   Next and iter are not currently implemented.

The asyncio built-in module makes it easy to port existing code that uses threads and blocking I/O over to coroutines
and asynchronous I/O.

See https://docs.python.or/3/library/asynchio.html for more information.
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


# Example 1:  First we construct a helper class for managing sending and receiving messages.
class EOFError(Exception):
    pass

class ConnectionBase:
    def __init__(self, connection):
        self.connection = connection
        self.file = connection.makefile('rb')

    def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.connection.send(data)

    def receive(self):
        line = self.file.readline()
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()


# Example 2:  We implement the server.   Handles one connection at a time and maintains the client's 
# session state.
import random

WARMER = 'Warmer'
COLDER = 'Colder'
UNSURE = 'Unsure'
CORRECT = 'Correct'

class UnknownCommandError(Exception):
    pass

class Session(ConnectionBase):
    def __init__(self, *args):
        # See Item 40 - super() solves the problem of superclass initialization and diamond inheritance.
        # See also:  https://en.wikipedia.org/wiki/Multiple_inheritance
        super().__init__(*args)  
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []


# Example 3:  Handles incoming commands and chooses the appropriate method
    def loop(self):
        while command := self.receive():
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                self.send_number()
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)


# Example 4:  Sets upper and lower boundaries for the guess.
    def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_state(lower, upper)


# Example 5:  Makes a new guess making sure the same number is not chosen.
    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    def send_number(self):
        guess = self.next_guess()
        self.guesses.append(guess)
        self.send(format(guess))


# Example 6:  Receives client decision and returns colder or warmer.
    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]

        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'Server: {last} is {decision}')


# Example 7:  Implement the client using a stateful class
import contextlib
import math

class Client(ConnectionBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None


# Example 8:  Sends first commands to server
    @contextlib.contextmanager
    def session(self, lower, upper, secret):
        print(f'Guess a number between {lower} and {upper}!'
              f' Shhhhh, it\'s {secret}.')
        self.secret = secret
        self.send(f'PARAMS {lower} {upper}')
        try:
            yield
        finally:
            self._clear_state()
            self.send('PARAMS 0 -1')


# Example 9:  New guesses are requested from the server.
    def request_numbers(self, count):
        for _ in range(count):
            self.send('NUMBER')
            data = self.receive()
            yield int(data)
            if self.last_distance == 0:
                return


# Example 10:  Reports whether a  guess is warmer or colder.
    def report_outcome(self, number):
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        self.send(f'REPORT {decision}')
        return decision


# Example 11:  Run the server.
import socket
from threading import Thread

def handle_connection(connection):
    with connection:
        session = Session(connection)
        try:
            session.loop()
        except EOFError:
            pass

def run_server(address):
    with socket.socket() as listener:
        # Allow the port to be reused
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(address)
        listener.listen()
        while True:
            connection, _ = listener.accept()
            thread = Thread(target=handle_connection,
                            args=(connection,),
                            daemon=True)
            thread.start()


# Example 12:  CLients runs in the main thread and returns the results.
def run_client(address):
    with socket.create_connection(address) as connection:
        client = Client(connection)

        with client.session(1, 5, 3):
            results = [(x, client.report_outcome(x))
                       for x in client.request_numbers(5)]

        with client.session(10, 15, 12):
            for number in client.request_numbers(5):
                outcome = client.report_outcome(number)
                results.append((number, outcome))

    return results


# Example 13:  Put everything together in main() and check if it works.
def main():
    address = ('127.0.0.1', 1234)
    server_thread = Thread(
        target=run_server, args=(address,), daemon=True)
    server_thread.start()

    results = run_client(address)
    for number, outcome in results:
        print(f'Client: {number} is {outcome}')

main()

print('********* End of program using threading *********')

# Example 14:  Now we refactor the code to use asyncio
# First we update ConnectionBase to provide coroutines.
class AsyncConnectionBase:  
    def __init__(self, reader, writer):             # Changed
        self.reader = reader                        # Changed
        self.writer = writer                        # Changed

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)                     # Changed
        await self.writer.drain()                   # Changed

    async def receive(self):
        line = await self.reader.readline()         # Changed
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()


# Example 15:  Create a session class for a single connection.
class AsyncSession(AsyncConnectionBase):            # Changed
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_values(None, None)

    def _clear_values(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []


# Example 16:  Need to add the await keyword
    async def loop(self):                           # Changed
        while command := await self.receive():      # Changed
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                await self.send_number()            # Changed
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)


# Example 17
    def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_values(lower, upper)


# Example 18:  Add async and await keywords
    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):                    # Changed
        guess = self.next_guess()
        self.guesses.append(guess)
        await self.send(format(guess))              # Changed


# Example 19
    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]

        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'Server: {last} is {decision}')


# Example 20:  Need to inherit from AsyncConnectioBase
class AsyncClient(AsyncConnectionBase):             # Changed
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None


# Example 21:  Need to use async context manager.
    @contextlib.asynccontextmanager                 # Changed
    async def session(self, lower, upper, secret):  # Changed
        print(f'Guess a number between {lower} and {upper}!'
              f' Shhhhh, it\'s {secret}.')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')  # Changed
        try:
            yield
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')          # Changed


# Example 22
    async def request_numbers(self, count):         # Changed
        for _ in range(count):
            await self.send('NUMBER')               # Changed
            data = await self.receive()             # Changed
            yield int(data)
            if self.last_distance == 0:
                return


# Example 23
    async def report_outcome(self, number):         # Changed
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        await self.send(f'REPORT {decision}')       # Changed
        # Make it so the output printing is in
        # the same order as the threaded version.
        await asyncio.sleep(0.01)
        return decision


# Example 24:  Nees to rewrite the code that runs the server.
import asyncio

async def handle_async_connection(reader, writer):
    session = AsyncSession(reader, writer)
    try:
        await session.loop()
    except EOFError:
        pass

async def run_async_server(address):
    server = await asyncio.start_server(
        handle_async_connection, *address)
    async with server:
        await server.serve_forever()


# Example 25:  Async keyword need here throughout
async def run_async_client(address):
    # Wait for the server to listen before trying to connect
    await asyncio.sleep(0.1)

    streams = await asyncio.open_connection(*address)   # New
    client = AsyncClient(*streams)                      # New

    async with client.session(1, 5, 3):
        results = [(x, await client.report_outcome(x))
                   async for x in client.request_numbers(5)]

    async with client.session(10, 15, 12):
        async for number in client.request_numbers(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))

    _, writer = streams                                 # New
    writer.close()                                      # New
    await writer.wait_closed()                          # New

    return results


# Example 26:  Use async create_task to glue the pieces together.
async def main_async():
    address = ('127.0.0.1', 4321)

    server = run_async_server(address)
    asyncio.create_task(server)

    results = await run_async_client(address)
    for number, outcome in results:
        print(f'Client: {number} is {outcome}')


logging.getLogger().setLevel(logging.ERROR)

asyncio.run(main_async())

logging.getLogger().setLevel(logging.DEBUG)

print('********* End of program using coroutines *********')