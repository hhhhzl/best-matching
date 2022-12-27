import time
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
from AssignNet.bipartite_matching.basic import Bipartite
from AssignNet.general_tools import Graph
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
    ope = Graph()
    G, weight = ope.add_edges(G, {})
    pprint.pprint(G)
    s = '0'
    t = '7'  # Read the source from disk
    graph = Bipartite(graph=G, source=s, sink=t)
    graph.execute()
    result = graph.result
    return result


if __name__ == "__main__":
    start = time.time()
    code_result = main(['test_data', 'out'])
    pprint.pprint(code_result)
    print(time.time() - start)
