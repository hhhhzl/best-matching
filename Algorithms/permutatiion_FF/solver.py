import pprint
import sys
import heapq
import numpy as np
from AssignNet.general_tools import Graph
import queue
from tools import Sort_Tuple


class PFF_SOLVER(Graph):
    def __init__(self, graph, directed):
        super().__init__()
        # residual graph

        self.directed = directed
        self.graph = graph
        self.parents = {}
        self.count = 0

    def permutation(self, graph, agentSet, objectSet, source=None, sink=None):
        c_graph = graph
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

    def BFS(self, s, t):
        distances = {}
        finalized = {}
        self.parents = {}
        layers = [[] for d in range(6)]
        Q = queue.Queue()
        distances[s] = 0
        self.parents[s] = None
        self.count += 1
        Q.put(s)
        while not (Q.empty()):
            u = Q.get()
            if u not in finalized:
                finalized[u] = True
                layers[distances[u]].append(u)
                for v in self.graph[u]:
                    if self.graph[u][v] > 0 and v not in distances:
                        if v == t:
                            distances[v] = distances[u] + 1
                            self.parents[v] = u
                            return True
                        else:
                            distances[v] = distances[u] + 1
                            self.parents[v] = u
                            Q.put(v)
        return False

    def Fold_fulkerson(self, s, t):
        # This array is filled by BFS and to store path
        max_flow = 0  # There is no flow initially
        # Augment the flow while there is path from source to sink
        while self.BFS(s, t):
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            last = t
            while last != s:
                path_flow = min(path_flow, self.graph[self.parents[last]][last])

                last = self.parents[last]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = t
            while v != s:
                u = self.parents[v]
                self.graph[u][v] -= path_flow

                if u not in self.graph[v]:
                    self.graph = self.add_edge(v, u, 0, self.graph)
                    self.graph[v][u] += path_flow
                    v = self.parents[v]
                else:
                    self.graph[v][u] += path_flow
                    v = self.parents[v]
        return max_flow
