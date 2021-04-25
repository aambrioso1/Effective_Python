"""
Item 68: Make pickle Reliable with copyreg

The pickle built-in module serializes Python objects into a stream of bytes and deserializes bytes back into objects.
Pickled byte streams should only be used between trusted parties.  The format is unsafe by design.

JSON also serializes data.  It is commonly used and human readable but it can be used with fewer python objects that pickle.
But can JSON is safe by design.  JSON should be used for communication between programs and people who don't trust each other.

The copyreg built-in module can be used with pickle to ensure backward compatibility for serialized objects.

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


# Example 1:  Create an object that represents the state of a player's progress in a game.
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4


# Example 2:  Create a instance of GameState and give it some values
state = GameState()
state.level += 1  # Player beat a level
state.lives -= 1  # Player had to try again

print(state.__dict__)


# Example 3:  Now we use the pickle module to store the game state.
import pickle

# We store serialize the game state and store iin a file using the dump method of the pickle module.
state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f) 


# Example 4:  We retrieve the file and deserialize it with the load method.
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# Example 5:  Now we expand the idea so that we can modifiy the GameState class a still work with the older
# pickle files.
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0  # New field


# Example 6:  Examples 6, 7, and 8 show that old files will be missing the new points attribute even though
# they are instances of the the new GameState class.
state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 7
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# Example 8
assert isinstance(state_after, GameState)


# Example 9:  Fix this problem first define the GameState object with default values so that it will always have 
# all the attributes after unpickling.
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


# Example 10:  Now we define a helper function that turns a GameState object into a tuple of parameters.
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


# Example 11:   And another helper function that takes serialized data and parameters and returns a GameState object
# with those parameters.
def unpickle_game_state(kwargs):
    return GameState(**kwargs)


# Example 12:   Now we register the functions using the built in copyreg module.
import copyreg

copyreg.pickle(GameState, pickle_game_state)


# Example 13:  Now we create an instance of GameState with points and pickle it.
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 14:  Next we add another attribute called magic.
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic  # New field


# Example 15:   Now the old GameState has the new format with the default value for magic (the new attribute).
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# Example 16:  This example, along with 17, shows that a backward incompatible change, like removing an
# atrribute will breakdown the deserialiation process.
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# Example 17
try:
    pickle.loads(serialized)
except:
    logging.exception('Expected')
else:
    assert False


# Example 18:   Using version numbers can solve this problem.   
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


# Example 19:  Now the unpickle function can use the version number to decide on its functionality.
# Here we remove the lives attribute.
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)


# Example 20:  One last problem is what to do if a class name changes.
copyreg.pickle(GameState, pickle_game_state)
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# Example 21
copyreg.dispatch_table.clear()
state = GameState()
serialized = pickle.dumps(state)
del GameState
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# Example 22
try:
    pickle.loads(serialized)
except:
    logging.exception('Expected')
else:
    assert False


# Example 23
print(serialized)


# Example 24:  By using copyreg we can specify a stable identifier for the function to use for unpickling an object.
# This will allow you to transition pickled data to different classes with different names when deserializing.
copyreg.pickle(BetterGameState, pickle_game_state)


# Example 25
state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized)