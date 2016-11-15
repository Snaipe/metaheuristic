import random
import sys

try:
    _seed = int(sys.argv[1])
except IndexError:
    _seed = random.randint(0, sys.maxsize)

_random = random.Random(_seed)

def get():
    return _random

def seed():
    return _seed
