import pprint
import numpy as np
import queue


class Graph:
    def __init__(self, graph=None, vertices=None, edges=None, matrix=None, directed=False, weighted=None):
        self.adj_list = {}
        self.adj_matrix = []
        self.num_vertices = 0
        self.isBipartite = None
        self.vertices = {}
        self.directed = directed
        self.weighted = weighted
        self.agentSet = []
        self.objectSet = []
        self.numb_agent = 0
        self.numb_object = 0
        self.sink = None
        self.source = None

        if graph is None:
            if edges is not None and matrix is None:
                if len(edges[0]) == 2:
                    self.weighted = False
                else:
                    self.weighted = True

                if vertices is None:
                    self.add_edges(edges)
                else:
                    self.add_vertices(vertices)
                    self.add_edges(edges)

            elif vertices is None and edges is None and matrix is not None:
                self.adj_matrix = np.array(matrix)
                self.matrix_to_adj()

        else:
            self.adj_list = graph
            vertices = list(self.adj_list.keys())
            self.add_vertices(vertices)

    # add edges to the graph
    def add_edges(self, edges):
        for edge in edges:
            if len(edge) == 2:
                self.add_edge(edge[0], edge[1])
            else:
                self.add_edge(edge[0], edge[1], edge[2])
        self.adj_to_matrix()

    # add vertices to the list
    def add_vertices(self, vertices_list):
        for node in vertices_list:
            if node not in self.vertices:
                self.vertices[node] = 1
                self.num_vertices += 1
                self.adj_list[node] = {}

    # get the vertex with its connections
    def get_vertex(self, node):
        if node in self.adj_list:
            return self.adj_list[node]
        else:
            print("Not Found")

    # add a single edge to the graph
    def add_edge(self, node1, node2, weight=0, graph=None):
        if graph is None:
            if node1 not in self.vertices:
                self.vertices[node1] = 1
                self.num_vertices += 1
                self.adj_list[node1] = {}
            if node2 not in self.vertices:
                self.vertices[node2] = 1
                self.num_vertices += 1
                self.adj_list[node2] = {}

            self.adj_list[node1][node2] = weight
            if not self.directed:
                self.adj_list[node2][node1] = weight
        else:
            graph[node1][node2] = weight
            return graph

    def get_vertices(self):
        return list(self.vertices.keys())

    def adj_to_matrix(self):
        number = len(self.adj_list.keys())
        self.adj_matrix = np.zeros((number, number), dtype=float)
        index_list = {}
        node_dic = {}
        for index, node in enumerate(self.vertices):
            index_list[index] = node
            node_dic[node] = index

        if self.weighted:
            for i in range(number):
                for j in self.adj_list[index_list[i]].keys():
                    self.adj_matrix[i][node_dic[j]] = self.adj_list[index_list[i]][j]
        else:
            for i in range(number):
                for j in self.adj_list[index_list[i]].keys():
                    self.adj_matrix[i][node_dic[j]] = 1

    def matrix_to_adj(self):
        row = self.adj_matrix.shape[0]
        col = self.adj_matrix.shape[1]
        for i in range(row):
            for j in range(col):
                if i != j or self.adj_matrix[i][j] != 0:
                    self.add_edge(str(i + 1), str(j + 1), self.adj_matrix[i][j])

    def print_graph(self):
        pprint.pprint(self.adj_list)
        print(self.adj_matrix)
        print(self.num_vertices)

    def check_bipartite(self):
        if self.vertices != {}:
            color = {}
            source = list(self.adj_list.keys())[0]
            color[source] = 1
            self.agentSet.append(source)
            self.numb_agent += 1
            Q = queue.Queue()
            Q.put(source)
            while not (Q.empty()):
                u = Q.get()
                for node in self.adj_list[u].keys():
                    if node not in color:
                        if color[u] == 1:
                            color[node] = 0
                            self.objectSet.append(node)
                            self.numb_object += 1
                        else:

                            color[node] = 1
                            self.agentSet.append(node)
                            self.numb_agent += 1
                        Q.put(node)
                    else:
                        if color[node] == color[u]:
                            self.agentSet = []
                            self.objectSet = []
                            self.numb_agent = 0
                            self.numb_object = 0
                            self.isBipartite = False
                            break
            self.isBipartite = True

    def check_sink_source(self, graph):
        pass


if __name__ == '__main__':
    m = [
        [0, 1, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0],
    ]
    v = ["a", 'b', 'c', 'd']
    E = [
        ('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'd'), ('a', 'c')
    ]
    g = Graph(matrix=m)
    g.print_graph()
    print(g.check_bipartite())
