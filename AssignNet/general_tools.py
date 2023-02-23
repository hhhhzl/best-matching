import pprint
import numpy as np
import queue
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import math

class Graph:
    def __init__(self):
        pass

    # add edges to the graph
    def add_edges(self, edges, graph):
        weighted = None
        for edge in edges:
            if len(edge) == 2:
                weighted = False
                self.add_edge(str(edge[0]), str(edge[1]), graph=graph)
            else:
                weighted = True
                self.add_edge(str(edge[0]), str(edge[1]), edge[2], graph=graph)
        return graph, weighted

    def get_vertices(self, graph):
        return list(graph.keys())

    def add_single_vertex_graph(self, graph, node):
        if node not in list(graph.keys()):
            graph[node] = {}
        return graph

    # add vertices to the list, input a vertices list,
    def add_vertices_to_graph(self, vertices_list):
        num_vertices = len(vertices_list)
        vertices = {}
        graph = {}
        for node in vertices_list:
            if node not in vertices:
                vertices[node] = 1
                graph[node] = {}
        return num_vertices, vertices, graph

    # get the vertex with its connections
    def get_vertex(self, node, graph):
        if node in graph:
            return graph[node]
        else:
            print("Not Found")

    # add a single edge to the graph
    def add_edge(self, node1, node2, weight=0, graph=None, directed=False):
        if node1 not in graph:
            graph[node1] = {}
        if node2 not in graph:
            graph[node2] = {}

        if directed:
            graph[node1][node2] = weight
            graph[node2][node1] = weight
        else:
            graph[node1][node2] = weight
        return graph

    def adj_to_matrix(self, graph, weighted):
        number = len(graph.keys())
        adj_matrix = np.zeros((number, number), dtype=float)
        index_list = {}
        node_dic = {}
        for index, node in enumerate(list(graph.keys())):
            index_list[index] = node
            node_dic[node] = index

        if weighted:
            for i in range(number):
                for j in graph[index_list[i]].keys():
                    adj_matrix[i][node_dic[j]] = graph[index_list[i]][j]
        else:
            for i in range(number):
                for j in graph[index_list[i]].keys():
                    adj_matrix[i][node_dic[j]] = 1
        return adj_matrix

    def matrix_to_adj(self, matrix):
        row = matrix.shape[0]
        col = matrix.shape[1]
        graph = {}
        for i in range(row):
            for j in range(col):
                if i != j or matrix[i][j] != 0:
                    graph = self.add_edge(str(i + 1), str(j + 1), matrix[i][j], graph)
        return graph

    def check_bipartite(self, graph, sink=None, Source=None):
        if graph != {}:
            if sink is None and Source is None:
                color = {}
                source = list(graph.keys())[0]
                color[source] = 1
                agentSet, objectSet = [], []
                numb_agent, numb_object = 0, 0
                agentSet.append(source)
                numb_agent += 1
                Q = queue.Queue()
                Q.put(source)
                while not (Q.empty()):
                    u = Q.get()
                    for node in graph[u].keys():
                        if node not in color:
                            if color[u] == 1:
                                color[node] = 0
                                objectSet.append(node)
                                numb_object += 1
                            else:

                                color[node] = 1
                                agentSet.append(node)
                                numb_agent += 1
                            Q.put(node)
                        else:
                            if color[node] == color[u]:
                                return False, 0, [], 0, []
                return True, numb_agent, agentSet, numb_object, objectSet
            elif sink is not None and Source is not None:
                color = {}
                source = list(graph.keys())[0]
                color[source] = 1
                agentSet, objectSet = [], []
                numb_agent, numb_object = 0, 0
                numb_agent += 0
                Q = queue.Queue()
                Q.put(source)
                while not (Q.empty()):
                    u = Q.get()
                    for node in graph[u].keys():
                        if node != sink and node != Source:
                            if node not in color:
                                if color[u] == 1:
                                    color[node] = 0
                                    agentSet.append(node)
                                    numb_object += 1
                                else:

                                    color[node] = 1
                                    objectSet.append(node)
                                    numb_agent += 1
                                Q.put(node)
                            else:
                                if color[node] == color[u]:
                                    return False, 0, [], 0, []
                return True, numb_agent, agentSet, numb_object, objectSet

    def add_sink_source_layer(self, graph, agentSet):
        source_dic = {}
        sink_dic = {}
        new = {}
        for node in agentSet:
            source_dic[node] = 1
        new[DEFAULT_SOURCE] = source_dic
        sink_dic[DEFAULT_SINK] = {}
        res = {**new, **graph, **sink_dic}
        return res

    def allow_multi_assign(self, graph, objectSet, agentSet, sink=None):
        if sink:
            number = len(agentSet) // len(objectSet) + 1
            for node in objectSet:
                graph[node][sink] = int(number)
            return graph

    def directed_check_agentSet(self, graph):
        agent = []
        for node in graph.keys():
            if graph[node] != {}:
                agent.append(node)
        return agent

    def check_set_numbers(self, graph, agentSet):
        agentOrder = {}
        for agent in agentSet:
            agentOrder[agent] = len(list(graph[agent].keys()))
        return agentOrder

    def generate_results(self, graph, agentSet, sink=None, source=None):
        result = []
        for node in agentSet:
            for i in graph[node].keys():
                if graph[node][i] == 0:
                    result.append((node, i))
        return result


if __name__ == '__main__':
    pass
