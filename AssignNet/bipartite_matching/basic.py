import copy
import pprint
import time

from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
from AssignNet.general_tools import Graph
from Algorithms.permutatiion_FF.solver import PFF_SOLVER

class test():
    def __init__(self):
        pass

    def test_fun(self):
        time.sleep(5)

class Bipartite(Graph):
    def __init__(self, graph=None, matrix=None, edges_list=None, directed=None, sink=None, source=None,
                 allow_multitask=True, method='PFF', permutation=True):
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
        self.agent_set = None
        self.object_set = None
        self.numb_agent = None
        self.numb_object = None
        self.permutation = permutation

    def execute(self):
        if self.graph and self.matrix is None and self.edges_list is None:
            self.run_graph()
        elif self.matrix and self.graph is None and self.edges_list is None:
            self.run_matrix()
        elif self.edges_list and self.graph is None and self.matrix is None:
            self.run_edges()

    def run_graph(self):
        if self.sink is not None and self.source is not None:
            valid, self.numb_agent, self.agent_set, self.numb_object, self.object_set = self.check_bipartite(
                graph=self.graph, sink=self.sink, Source=self.source)
            if valid:
                if self.allow_multi:
                    self.graph = self.allow_multi_assign(self.graph, objectSet=self.object_set, sink=self.sink)
                # add methods
                if self.method == "PFF":
                    graph = PFF_SOLVER(self.graph, True, self.numb_agent+self.numb_object)
                    if self.permutation:
                        graph.permutation(graph=graph.graph, agentSet=self.agent_set, objectSet=self.object_set, sink=self.sink, source=self.source)
                    graph.Fold_fulkerson(self.source, self.sink)
                    self.result = graph.graph
                else:
                    self.result = "Invalid Method."
            else:
                self.result = 'Graph is not Bipartite.'

        elif (self.sink is not None and self.source is None) or (self.sink is None and self.source is not None):
            self.result = "Please Enter the sink and source together."

        else:
            if self.directed:
                self.agent_set = self.directed_check_agentSet(self.graph)
                self.graph = self.add_sink_source_layer(graph=self.graph, agentSet=self.agent_set)  # add layer
                self.source = DEFAULT_SOURCE
                self.sink = DEFAULT_SINK
                valid, self.numb_agent, self.agent_set, self.numb_object, self.object_set = self.check_bipartite(
                    graph=self.graph, sink=self.sink, Source=self.source)
                if valid:
                    if self.allow_multi:
                        self.graph = self.allow_multi_assign(self.graph, objectSet=self.object_set, sink=self.sink)
                    if self.method == "PFF":
                        graph = PFF_SOLVER(self.graph, True, self.numb_agent+self.numb_object)
                        if self.permutation:
                            graph.permutation(graph=graph.graph, agentSet=self.agent_set, objectSet=self.object_set, sink=self.sink, source=self.source)
                        graph.Fold_fulkerson(self.source, self.sink)
                        self.result = graph.graph
                    else:
                        self.result = "Invalid Method."
                else:
                    self.result = 'Graph is not Bipartite.'

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
