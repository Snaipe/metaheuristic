import math

from . import random

_random = random.get()

def gen(g, cols, rows):
    return [(i % cols, i // rows) for i in range(0, len(g.nodes()))]

def mutate(i, cols, rows, n=1):
    mutations = set()
    for j in range(0, n):
        while True:
            first = _random.randrange(len(i))
            while True:
                direction = _random.randrange(4) * math.pi / 2
                second = int(first + math.cos(direction) + cols * math.sin(direction))
                if abs(second % cols - first % cols) <= 1 and second < (cols * rows) and second >= 0:
                    break
            if (first, second) not in mutations:
                break
        i[first], i[second] = i[second], i[first]
    return i

def randomize(i, n=1):
    for j in range(0, n):
        first = _random.randrange(len(i))
        second = _random.randrange(len(i))
        while first == second:
            second = _random.randrange(len(i))
        i[first], i[second] = i[second], i[first]
    return i

def cost(g, indiv, weight):
    dist = 0
    for u, v in g.edges():
        dist += (abs(indiv[u][0] - indiv[v][0]) + abs(indiv[u][1] - indiv[v][1])) * weight
    return dist

