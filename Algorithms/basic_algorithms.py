import sys
import heapq
import numpy as np
import queue



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
                if v not in distances:  # first path to v
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
