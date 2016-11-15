import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cbook
import warnings

warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def random(nodes, maxedges=None, seed=None):
    if maxedges is None:
        maxedges = nodes * (nodes - 1)
    return nx.gnm_random_graph(nodes, random.randint(nodes, maxedges), seed)

def show(g,pos=None,rows=None,cols=None,orig=(0,0),update=True):
    if pos is None:
        pos = [((i % cols), i // rows) for i in range(0, cols * rows)]
    if update:
        plt.clf()
    p = [(x + orig[0], y - orig[1]) for x, y in pos]
    nx.draw_networkx_nodes(g,p)
    nx.draw_networkx_edges(g,p)
    nx.draw_networkx_labels(g,p)
    plt.axis('off')
    if update:
        plt.pause(0.00001)

def regular_grid(cols, rows):
    g = nx.Graph()
    g.add_nodes_from(list(range(0, rows * cols)))

    for i in range(0, cols - 1):
        for j in range(0, rows - 1):
            g.add_edge(i + j * cols, i + 1 + j * cols)
            g.add_edge(i + j * cols, i + (j + 1) * cols)

    for i in range(0, rows - 1):
        g.add_edge((cols - 1) + i * cols, (cols - 1) + (i + 1) * cols)

    for i in range(0, cols - 1):
        g.add_edge(i + (rows - 1) * cols, i + 1 + (rows - 1) * cols)
    return g
