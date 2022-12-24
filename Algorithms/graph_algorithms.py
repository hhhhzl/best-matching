import sys
import heapq
import numpy as np
import AssignNet.simple_graph_operations as sg
import queue


class AssignmentProblem:
    def __init__(self, graph):
        # residual graph
        self.graph = graph
        self.parents = {}
        self.count = 0

    def BFS(self, s, t):
        distances = {}
        finalized = {}
        self.parents = {}
        layers = [[] for d in range(self.graph["n"])]
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
                for v in self.graph["adj"][u]:
                    if self.graph["adj"][u][v] > 0 and v not in distances:
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
                path_flow = min(path_flow, self.graph['adj'][self.parents[last]][last])

                last = self.parents[last]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = t
            while v != s:
                u = self.parents[v]

                self.graph['adj'][u][v] -= path_flow

                if u not in self.graph['adj'][v]:
                    self.graph = sg.addDirEdge(self.graph, v, u, 0)
                    self.graph['adj'][v][u] += path_flow
                    v = self.parents[v]
                else:
                    self.graph['adj'][v][u] += path_flow
                    v = self.parents[v]
        return max_flow


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
    return


############################################################
# Traversals
############################################################

def BFS(G, s):
    # G is a dictionary with keys "n", "m", "adj" representing an unweighted graph
    # G["adj"][u][v] is True if (u,v) is present. Otherwise, v is not in G["ad"][u].
    distances = {}
    finalized = {}  # set of discovered nodes
    parents = {}  # lists parent of node in SP tree
    layers = [[] for d in range(G["n"])]  # lists of nodes at each distance.
    Q = queue.Queue()
    distances[s] = 0
    parents[s] = None
    Q.put(s)
    while not (Q.empty()):  # Q not empty
        u = Q.get()
        if u not in finalized:  # if u was already finalized, ignore it.
            finalized[u] = True
            layers[distances[u]].append(u)
            for v in G["adj"][u]:
                # record v's distance and parent and add v to the queue if
                # this is the first path to v,
                if (v not in distances):  # first path to v
                    distances[v] = distances[u] + 1
                    parents[v] = u
                    Q.put(v)
    return distances, parents, layers


def DFS(G):
    color = {}
    discovered = {}
    finished = {}
    parent = {}
    for u in G["adj"]:
        color[u] = "white"
        parent[u] = None
    timestamp = [0]  # This is a list whose only element is the current value of the time stamp.

    def DFSVisit(u, G, timestamp, color, discovered, finished):
        # Only the first argument ever changes
        color[u] = "gray"
        timestamp[0] = timestamp[0] + 1
        discovered[u] = timestamp[0]
        for v in G["adj"][u]:
            if color[v] == "white":
                parent[v] = u
                DFSVisit(v, G, timestamp, color, discovered, finished)
        color[u] = "black"
        timestamp[0] = timestamp[0] + 1
        finished[u] = timestamp[0]
        return

    for u in G["adj"]:
        if color[u] == "white":
            DFSVisit(u, G, timestamp, color, discovered, finished)
    return discovered, finished, parent


def dijkstra(G, s):
    # G is a dictionary with keys "n", "m", "adj" representing an *weighted* graph
    # G["adj"][u][v] is the cost (length / weight) of edge (u,v)
    # These algorithms finds least-costs paths to all vertices
    # Returns an array of distances (path costs) and parents in the lightest-paths tree.
    # Assumes non-negative path costs
    distances = {}  # actual distances
    finalized = {}  # set of discovered nodes
    parents = {}  # lists parent of node in SP tree
    Q = []  # empty priority queue. Use heappush(Q, (priorit, val)) to add. Use heappop(Q) to remove.
    distances[s] = 0
    parents[s] = None
    heapq.heappush(Q, (distances[s], s))
    while len(Q) > 0:  # Q not empty
        (d, u) = heapq.heappop(Q)
        if u not in finalized:  # if u was already finalized, ignore it.
            finalized[u] = True
            for v in G["adj"][u]:
                new_length = distances[u] + G["adj"][u][v]
                # update v's distance (and parent and priority queue) if
                # either this is the first path to v
                # or we have found a better path to v
                if (v not in distances) or (new_length < distances[v]):
                    distances[v] = new_length
                    parents[v] = u
                    # add a copy of v to the queue with priority distances[v]
                    heapq.heappush(Q, (distances[v], v))
    return distances, parents
