import pprint
import sys
import heapq
import numpy as np
from AssignNet.general_tools import Graph
import queue
from tools import Sort_Tuple
import copy
import numpy as np
from numba import njit
from numba.experimental import jitclass


def add_edge_s(node1, node2, weight=0, graph=None, directed=False):
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

def BFS(graph, parents, s, t, n, count):
    distances = {}
    finalized = {}
    parents = {}
    layers = [[] for d in range(n)]
    Q = queue.Queue()
    distances[s] = 0
    parents[s] = None
    count += 1
    Q.put(s)
    while not (Q.empty()):
        u = Q.get()
        if u not in finalized:
            finalized[u] = True
            layers[distances[u]].append(u)
            for v in graph[u]:

                if graph[u][v] > 0 and v not in distances:
                    if v == t:
                        distances[v] = distances[u] + 1
                        parents[v] = u
                        return True, graph, parents, count
                    else:
                        distances[v] = distances[u] + 1
                        parents[v] = u
                        Q.put(v)
    return False, graph, parents, count

@njit
def run_FF(graph, parents, s, t, n, count):
    # This array is filled by BFS and to store path
    max_flow = 0  # There is no flow initially
    # Augment the flow while there is path from source to sink
    valid, graph, parents, count = BFS(graph, parents, s, t, n, count)
    while valid:
        # Find minimum residual capacity of the edges along the
        # path filled by BFS. Or we can say find the maximum flow
        # through the path found.
        path_flow = float("Inf")
        last = t
        while last != s:
            path_flow = min(path_flow, graph[parents[last]][last])

            last = parents[last]

        # Add path flow to overall flow
        max_flow += path_flow

        # update residual capacities of the edges and reverse edges
        # along the path
        v = t
        while v != s:
            u = parents[v]
            graph[u][v] -= path_flow

            if u not in graph[v]:
                graph = add_edge_s(node1=v, node2=u, weight=0, graph=graph)
                graph[v][u] += path_flow
                v = parents[v]
            else:
                graph[v][u] += path_flow
                v = parents[v]
        valid, graph, parents, count = BFS(graph, parents, s, t, n, count)
    return max_flow

def ford_ff(graph, s, t, n):
    count = 0
    return run_FF(graph, {}, s, t, n, count)

class PFF_SOLVER(Graph):
    def __init__(self, graph=None, directed=None, n=None):
        super().__init__()
        # residual graph
        self.n = n
        self.directed = directed
        self.graph = graph
        self.parents = {}
        self.count = 0

    def permutation(self, graph, agentSet, objectSet, source=None, sink=None):
        objectOrder = {}
        agentOrder = {}
        for agent in agentSet:
            agentOrder[agent] = len(list(graph[agent].keys()))
            for object in graph[agent].keys():
                if object != source:
                    if object not in objectOrder:
                        objectOrder[object] = 1
                    else:
                        objectOrder[object] += 1

        for agent in agentSet:
            for object in graph[agent].keys():
                if object == source:
                    graph[agent][object] = (object, graph[agent][object], 0)
                else:
                    graph[agent][object] = (object, graph[agent][object], objectOrder[object])
            new_dic = graph[agent]
            new_list = Sort_Tuple(list(new_dic.values()))
            new_dic = {}
            for node in new_list:
                new_dic[node[0]] = node[1]
            graph[agent] = new_dic
        self.graph = graph
        return graph

    def Fold_fulkerson(self, s, t):
        return run_FF(self.graph, self.parents, s, t, self.n, self.count)
