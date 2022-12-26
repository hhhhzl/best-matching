import time

import simple_graph_operations as sg
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
import pprint
from tools.read_graph_tools import readGraph


def main(args=[]):
    # Expects three command-line arguments:
    # 1) name of a file describing the graph
    # 2) name of a file with the ID of the start node
    # 3) name of a file where the output should be written
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 3.".format(len(args)))
        return
    graph_file = args[0]
    out_file = args[1]

    G = readGraph(graph_file, True)  # Read the graph from disk
    s = 0
    t = 7  # Read the source from disk
    G.check_bipartite()
    graph = PFF_SOLVER(G.adj_list, True)
    result = graph.Fold_fulkerson(s, t)
    final_graph = graph.graph
    return result, final_graph


if __name__ == "__main__":
    start = time.time()
    code_result, graph = main(['test_data', 'out'])
    print(code_result)
    pprint.pprint(graph)
    print(time.time() - start)
