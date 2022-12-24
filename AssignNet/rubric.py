import simple_graph_operations as sg
from Algorithms.graph_algorithms import AssignmentProblem
import pprint


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
    G = sg.readGraph(graph_file)  # Read the graph from disk
    s = 0
    t = 7 # Read the source from disk
    graph = AssignmentProblem(G)
    pprint.pprint(G)
    result = graph.Fold_fulkerson(s, t)

    final_graph = graph.graph
    # analysis = final_graph['adj'][10000]
    # print(analysis)
    # list = []
    # for key in analysis:
    #     list.append(analysis[key])
    # list = np.array(list)
    # print(np.mean(list))
    # print(np.std(list))
    ##--------------------------------------------------------------------------------------##
    # hole_found, hole_length, hole_list = shortestHole(G, s)  # Find the shortest hole!
    # writeOutput(out_file, hole_found, hole_length, hole_list)  # Write the output
    return result, final_graph


if __name__ == "__main__":
    code_result, graph = main(['test_data', 'out'])
    print(code_result)
    pprint.pprint(graph['adj'])
