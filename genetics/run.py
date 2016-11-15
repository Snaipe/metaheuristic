#!/usr/bin/env python3
import matplotlib.pyplot as plt
import math
import itertools

from commons import graph
from commons import random
from commons import mutation

from config import *

NODES = ROWS * COLS

print('seed = ', random.seed())
random = random.get()

plt.ion()
plt.show()

def gen_pop(g, n, muts=NODES * NODES):
    pop = [mutation.randomize(mutation.gen(g, COLS, ROWS), muts) for i in range(0, n)]
    return ((mutation.cost(g, e, EDGE_WEIGHT), e) for e in pop)

def sort_pop(g, pop):
    return list((mutation.cost(g, k, EDGE_WEIGHT), k) for k,_ in itertools.groupby(sorted(pop), key=lambda x: x[1]))[:POPULATION]

def correct_child(major, child, pivot):
    taken = set()
    avail = {i for i in range(0, len(child))}
    for i in range(0, pivot):
        taken.add(major[i])
    for i in range(0, len(child)):
        avail.discard(child[i])

    for i in range(pivot, len(child)):
        if child[i] in taken:
            child[i] = avail.pop()
        taken.add(child[i])

    return mutation.mutate([(i % COLS, i // ROWS) for i in child], COLS, ROWS, random.randint(MIN_MUTATIONS_PER_CHILD, MAX_MUTATIONS_PER_CHILD))

def breed(g, father, mother):
    father = [x + y * COLS for x, y in father]
    mother = [x + y * COLS for x, y in mother]

    old_pivots = set()
    for i in range(0, BREED_COUNT):
        pivot = random.randrange(1, len(father) - 1)
        while pivot in old_pivots:
            pivot = random.randrange(1, len(father) - 1)
        old_pivots.add(pivot)

        children = father[:pivot] + mother[pivot:], mother[:pivot] + father[pivot:]

        child = correct_child(father, children[0], pivot)
        yield mutation.cost(g, child, EDGE_WEIGHT), child
        child = correct_child(mother, children[1], pivot)
        yield mutation.cost(g, child, EDGE_WEIGHT), child

def cross_excl(start, stop):
    for i in range(0, BEST_FIT):
        for j in range(0, BEST_FIT):
            if i != j:
                yield i, j

def next_gen(g, pop):
    pop = pop[:BEST_FIT] + [item for i, j in cross_excl(0, BEST_FIT)
                                 for item in breed(g, pop[i][1], pop[j][1])] \
              + list(gen_pop(g, RANDOM_GENERATION))
    return pop

def update(g, pop, epoch):
    print('epoch ' + str(epoch) + ': optimum = ' + str(pop[0][0]))
    plt.clf()
    for p in range(0, PRINT_FIRST):
        graph.show(g, pop[int(p * ((len(pop) - 1) / 3))][1], orig=((p % 2) * 5, (p // 2) * 5), update=False)
    plt.pause(0.0005)
    plt.savefig("epoch-" + str(epoch) + ".png")

def optimize(g, target, max_epoch):
    pop = sort_pop(g, gen_pop(g, POPULATION))
    mini = pop[0]
    epoch = 0

    if UPDATES > 0:
        freq = EPOCH / UPDATES
        update(g, pop, epoch)

    while mini[0] > target and epoch < max_epoch:
        pop = sort_pop(g, next_gen(g, pop))
        mini = min(mini, pop[0], key=lambda x: x[0])
        epoch += 1

        if UPDATES > 1 and epoch // freq > (epoch - 1) // freq:
            update(g, pop, epoch)

    return mini, epoch

G = graph.regular_grid(COLS, ROWS)

best, epoch = optimize(G, TARGET, EPOCH)

print('found optimum', best[0], 'after', epoch, 'generations.')
graph.show(G, best[1])
plt.savefig("result.png")
input()
