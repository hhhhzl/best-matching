import time
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
from AssignNet.bipartite_matching.basic import Bipartite
from AssignNet.general_tools import Graph
import pprint
from tools.read_graph_tools import readGraph


def percent_cal(agent_set, object_set, result, method):
    appearance = {}
    total = {}
    for i in agent_set:
        total[i] = 0
    for i in object_set:
        total[i] = 0

    for each_pair in result:
        if each_pair[0] not in appearance:
            appearance[each_pair[0]] = 1
        else:
            appearance[each_pair[0]] += 1
        if each_pair[1] not in appearance:
            appearance[each_pair[1]] = 1
        else:
            appearance[each_pair[1]] += 1

        total[each_pair[0]] = 1
        total[each_pair[1]] = 1

    percentage = sum(total.values()) / len(list(total.keys()))
    print(percentage)


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
    # ope = Graph()
    # g, weight = ope.add_edges(G, {})
    # s = '0'
    # t = '7'  # Read the source from disk

    graph = Bipartite(edges_list=G, directed=True, permutation=False, allow_multitask=True)
    graph.execute()
    result = graph.result
    final_result = graph.generate_results(result, agentSet=graph.agent_set)
    pprint.pprint(final_result)
    percent_cal(graph.agent_set, graph.object_set, final_result, "FFA")

    graph = Bipartite(edges_list=G, directed=True, permutation=True, allow_multitask=True)
    graph.execute()
    result = graph.result
    final_result = graph.generate_results(result, agentSet=graph.agent_set)
    pprint.pprint(final_result)
    percent_cal(graph.agent_set, graph.object_set, final_result, "PFFA")
    return final_result


if __name__ == "__main__":
    start = time.time()
    code_result = main(['test_data', 'out'])
    print(time.time() - start)
