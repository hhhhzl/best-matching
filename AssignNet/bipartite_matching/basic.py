from AssignNet.general_tools import Graph
from Algorithms.permutatiion_FF.solver import PFF_SOLVER


class Bipartite(Graph):
    def __init__(self, graph=None, sink=None, source=None, allow_multitask=False, method='PFF'):
        super().__init__()
        self.graph = graph
        self.symmetric = None
        self.sink = sink
        self.source = source
        self.allow_multi = allow_multitask
        self.method = method
        self.check_bipartite()
        if self.numb_agent != self.numb_object:
            self.symmetric = False
        else:
            self.symmetric = True
        self.result = None

    def execute(self):
        if self.sink is not None and self.source is not None:
            if self.method == "PFF":
                self.check_bipartite()
                graph = PFF_SOLVER(self.graph, True)
                result = graph.Fold_fulkerson(self.sink, self.source)
                self.result = graph.graph
            else:
                self.result = "Invalid Method"

        elif (self.sink is not None and self.source is None) or (self.sink is None and self.source is not None):
            self.result = "Please Enter the sink and source together."

        else:
            # add sink or source
            if self.method == "PFF":
                self.check_bipartite()
                graph = PFF_SOLVER(self.graph, True)
                result = graph.Fold_fulkerson(self.sink, self.source)
                self.result = graph.graph
            else:
                self.result = "Invalid Method"


