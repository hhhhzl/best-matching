import sys
import heapq
import numpy as np
import AssignNet.simple_graph_operations as sg
from AssignNet.general_tools import Graph
import queue


class PFF_SOLVER(Graph):
    def __init__(self, graph, directed):
        super().__init__()
        # residual graph

        self.directed = directed
        self.graph = graph
        self.parents = {}
        self.count = 0

    def permutation(self):
        pass

    def BFS(self, s, t):
        distances = {}
        finalized = {}
        self.parents = {}
        layers = [[] for d in range(3)]
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