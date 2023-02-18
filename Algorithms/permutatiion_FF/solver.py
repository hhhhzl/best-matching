import pprint
import sys
import heapq
import numpy as np
from AssignNet.general_tools import Graph
import queue
from tools import Sort_Tuple
import copy


class PFF_SOLVER(Graph):
    def __init__(self, graph=None, directed=None, n=None):
        super().__init__()
        # residual graph
        self.n = n
        self.directed = directed
        self.graph = graph
        self.parents = {}
        self.count = 0
        self.objectPrice = None
        self.objectOrder = None
        self.orderMax = 0
        self.eps = 0.01

    def permutation(self, graph, agentSet, objectSet, source=None, sink=None):
        objectPrice = {}
        agentOrder = {}
        objectOrder = {}
        for agent in agentSet:
            agentOrder[agent] = len(list(graph[agent].keys()))
            for object in graph[agent].keys():
                if object != source:
                    if object not in objectPrice:
                        objectPrice[object] = 1
                    else:
                        objectPrice[object] += 1

        order = {}
        for node in objectPrice.keys():
            order[node] = (node, objectPrice[node])

        order_list = Sort_Tuple(list(order.values()))
        for i in range(len(order_list)):
            objectOrder[order_list[i][0]] = i + 1

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
        self.objectPrice = objectPrice
        self.objectOrder = objectOrder
        return graph

    def permutation_in_PFFA(self, graph, agentSet, current, time, source=None):
        self.objectPrice, self.objectOrder = self.detect_change_order(self.objectPrice, current, time)
        for agent in agentSet:
            for object in graph[agent].keys():
                if object == source:
                    graph[agent][object] = (object, graph[agent][object], 0)
                else:
                    graph[agent][object] = (object, graph[agent][object], self.objectOrder[object])
            new_dic = graph[agent]
            new_list = Sort_Tuple(list(new_dic.values()))
            new_dic = {}
            for node in new_list:
                new_dic[node[0]] = node[1]
            graph[agent] = new_dic
        return graph

    def detect_change_order(self, objectPrice, current, time):
        objectPrice[current] += 1 + time * self.eps
        objectOrder = {}
        order = {}
        for node in objectPrice.keys():
            order[node] = (node, objectPrice[node])

        order_list = Sort_Tuple(list(order.values()))
        for i in range(len(order_list)):
            objectOrder[order_list[i][0]] = i + 1
        return objectPrice, objectOrder

    def BFS(self, s, t):
        distances = {}
        finalized = {}
        self.parents = {}
        layers = [[] for d in range(self.n)]
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

    def Fold_fulkerson(self, s, t, agentSet):
        # This array is filled by BFS and to store path
        max_flow = 0  # There is no flow initially
        # Augment the flow while there is path from source to sink
        request = 0
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
            current_node = None
            counter = 0

            while v != s:
                u = self.parents[v]
                if counter == 0:
                    current_node = u
                self.graph[u][v] -= path_flow

                if u not in self.graph[v]:
                    self.graph = self.add_edge(node1=v, node2=u, weight=0, graph=self.graph)
                    self.graph[v][u] += path_flow
                    v = self.parents[v]
                else:
                    self.graph[v][u] += path_flow
                    v = self.parents[v]
                counter += 1
            self.graph = self.permutation_in_PFFA(graph=self.graph, source=s, agentSet=agentSet, current=current_node, time=request)
            request += 1
        return max_flow