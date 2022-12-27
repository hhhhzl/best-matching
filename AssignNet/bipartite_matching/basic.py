import pprint

from AssignNet.general_tools import Graph
from Algorithms.permutatiion_FF.solver import PFF_SOLVER


class Bipartite(Graph):
    def __init__(self, graph=None, matrix=None, edges_list=None, directed=None, sink=None, source=None,
                 allow_multitask=False, method='PFF'):
        super().__init__()
        self.weighted = None
        self.graph = graph
        self.matrix = matrix
        self.edges_list = edges_list
        self.symmetric = None
        self.sink = sink
        self.source = source
        self.allow_multi = allow_multitask
        self.method = method
        self.directed = directed
        self.result = None

    def execute(self):
        if self.graph and self.matrix is None and self.edges_list is None:
            self.run_graph()
        elif self.matrix and self.graph is None and self.edges_list is None:
            self.run_matrix()
        elif self.edges_list and self.graph is None and self.matrix is None:
            self.run_edges()

    def run_graph(self):
        if self.sink is not None and self.source is not None:
            if self.method == "PFF":
                graph = PFF_SOLVER(self.graph, True)
                graph.permutation(graph.graph, ['1', '2', '3'], ['4', '5', '6'], '0', '7')
                graph.Fold_fulkerson(self.source, self.sink)
                self.result = graph.graph
            else:
                self.result = "Invalid Method."

        elif (self.sink is not None and self.source is None) or (self.sink is None and self.source is not None):
            self.result = "Please Enter the sink and source together."

        else:
            # add sink or source
            if self.method == "PFF":
                self.check_bipartite(self.graph)
                graph = PFF_SOLVER(self.graph, True)
                result = graph.Fold_fulkerson(self.sink, self.source)
                self.result = graph.graph
            else:
                self.result = "Invalid Method."

    def run_edges(self):
        if len(self.edges_list[0]) == 2:
            self.edges_list = [node + [1] for node in self.edges_list]
            self.graph, self.weighted = self.add_edges(edges=self.edges_list, graph={})
            self.run_graph()
        else:
            self.graph, self.weighted = self.add_edges(edges=self.edges_list, graph={})
            self.run_graph()

    def run_matrix(self):
        pass
