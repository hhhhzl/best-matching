import numpy as np
from AssignNet.general_tools import Graph

def readSource(start_file):
    # The source vertex is listed in its own file
    # It is an integer on a line by itself.
    with open(start_file, 'r') as f:
        raw_start = f.readline()
        s = int(raw_start)
    return s


def writeOutput(output_file, hole_found, hole_length, hole_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n".format(hole_found))
        f.write("{}\n".format(hole_length))
        f.write("{}\n".format(hole_list))


def readGraph(input_file, directed):
    '''This procedure takes the name of a text file describing a directed or undirected graph and returns a data structure in memory.
    The file is structured as follows: each line lists an edge as a pair u,v, for an unweighted graph, or triples u,v,w for a weighted graph, where w represents the edge's weight as a float.
    The data structure it returns is a dictionary with keys "n", "m", "adj" (strings). The values for "n" and "m" are the number of nodes and edges in the graph (respectively). Edges are counted as in a directed graph (so each undirected edge counts twice). The value for "adj" is a dictionary-of-dictionaries adjacency structure.
    '''
    with open(input_file, 'r') as f:
        raw = [[int(x) for x in s.split(', ')] for s in f.read().splitlines()]
    return raw


def writeGraph(G, output_file):
    # G is a dictionary with keys "n", "m", "adj" representing a
    # weighted or unweighted graph
    with open(output_file, 'w') as f:
        for u in G["adj"].keys():
            for v in G["adj"][u]:
                if G["adj"][u][v] == True:
                    f.write("{}, {}\n".format(u, v))
                else:
                    f.write("{}, {}, {}\n".format(u, v, G["adj"][u][v]))
    return