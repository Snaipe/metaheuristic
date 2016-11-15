#!/usr/bin/env python3
import matplotlib.pyplot as plt
import math
import copy

from commons import graph
from commons import random
from commons import mutation

from config import *

NODES = ROWS * COLS

print('seed = ', random.seed())
random = random.get()

plt.ion()
plt.show()

def make_state(g):
    state = mutation.randomize(mutation.gen(g, COLS, ROWS), NODES * NODES)
    return mutation.cost(g, state, EDGE_WEIGHT), state

def update(g, state, epoch, temp, acceptance=1, improvement=1):
    tmpsig = int(math.log10(TMAX) - math.log10(TMIN))
    print('epoch ' + ('%' + str(math.log10(EPOCH) + 1) + 'd') % epoch + ': optimum =', state[0], 'T∘ =', \
          (('{0:.' + str(tmpsig) + 'g}').format(temp) + ' ' * tmpsig)[:tmpsig + 1] + '\t', \
          '✓', '{0:.3g}'.format(acceptance * 100.), '🡹', '{0:.3g}'.format(improvement * 100.))
    graph.show(g, state[1])
    plt.savefig("epoch-" + str(epoch) + ".png")

def move(g, state):
    indiv = mutation.randomize(state[1])
    return mutation.cost(g, indiv, EDGE_WEIGHT), indiv

def optimize(g):

    epoch = 0
    state = make_state(g)
    prev, best = copy.deepcopy(state), copy.deepcopy(state)

    tfactor = -math.log(TMAX / TMIN)
    temp = TMAX

    trials, accepts, improves = 0, 0, 0
    if UPDATES > 0:
        freq = EPOCH / UPDATES
        update(g, state, epoch, temp)

    while epoch < EPOCH:
        temp = TMAX * math.exp(tfactor * epoch / EPOCH)
        state = move(g, state)

        costdiff = state[0] - prev[0]
        trials += 1
        if costdiff > 0 and math.exp(-costdiff / temp) < random.random():
            state = copy.deepcopy(prev)
        else:
            accepts += 1
            if costdiff < 0:
                improves += 1
            prev = copy.deepcopy(state)
            if state[0] < best[0]:
                best = copy.deepcopy(state)

        epoch += 1

        if UPDATES > 1 and epoch // freq > (epoch - 1) // freq:
            update(g, state, epoch, temp, accepts / trials, improves / trials)
            trials, accepts, improves = 0, 0, 0

    return best

G = graph.regular_grid(COLS, ROWS)

best = optimize(G)

print('found optimum', best[0])
graph.show(G, best[1], cols=COLS, rows=ROWS)
plt.savefig("result.png")
input()
