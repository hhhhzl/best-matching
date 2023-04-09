import pprint
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
from AssignNet.general_tools import Graph
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
import copy
import numpy as np
from AssignNet.bipartite_matching.basic import Bipartite, test
import concurrent.futures
import time
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import string
import logging
import copy

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class Trans_Problem(Graph):
    def __init__(self, graph=None, matrix=None, edges_list=None, directed=None, sink=None, source=None,
                 allow_multitask=True, method='PFF', permutation=True):
        super().__init__()
        self.weighted = None
        self.directed = directed
        self.method = method
        self.graph = graph
        self.matrix = matrix
        self.edges_list = edges_list
        self.sink = sink
        self.source = source
        self.allow_multi = allow_multitask

        self.symmetric = None
        self.result = None
        self.agent_set = None
        self.object_set = None
        self.numb_agent = None
        self.numb_object = None
        self.permutation = permutation
        self.layering_graph = None
        self.string_dic = {}
        self.used_dic = {}

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
                    self.graph = self.allow_multi_assign(self.graph, objectSet=self.object_set, sink=self.sink,
                                                         agentSet=self.agent_set)
                # add methods
                if self.method == "PFF":
                    graph = PFF_SOLVER(self.graph, True, self.numb_agent + self.numb_object)
                    if self.permutation:
                        graph.permutation(graph=graph.graph, agentSet=self.agent_set, objectSet=self.object_set,
                                          sink=self.sink, source=self.source)
                    graph.Fold_fulkerson(self.source, self.sink, agentSet=self.agent_set)
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
                self.graph = add_sink_source_layer(graph=self.graph, agentSet=self.agent_set)  # add layer
                self.source = DEFAULT_SOURCE
                self.sink = DEFAULT_SINK
                valid, self.numb_agent, self.agent_set, self.numb_object, self.object_set = self.check_bipartite(
                    graph=self.graph, sink=self.sink, Source=self.source)
                if valid:
                    if self.allow_multi:
                        self.graph = self.allow_multi_assign(self.graph, objectSet=self.object_set, sink=self.sink,
                                                             agentSet=self.agent_set)
                    if self.method == "PFF":
                        graph = PFF_SOLVER(self.graph, True, self.numb_agent + self.numb_object)
                        if self.permutation:
                            graph.permutation(graph=graph.graph, agentSet=self.agent_set, objectSet=self.object_set,
                                              sink=self.sink, source=self.source)
                        graph.Fold_fulkerson(self.source, self.sink, agentSet=self.agent_set)
                        self.result = graph.graph
                    else:
                        self.result = "Invalid Method."
                else:
                    self.result = 'Graph is not Bipartite.'

    def run_edges(self):
        self.graph, self.weighted = self.add_edges(edges=self.edges_list, graph={})
        self.run_graph()

    def run_matrix(self):
        pass

    def layering(self, graph, source, agent_set):
        if agent_set is None:
            valid, self.numb_agent, self.agent_set, self.numb_object, self.object_set = self.check_bipartite(
                graph=graph, sink=self.sink, Source=self.source)
        agentSet_connects = self.check_set_numbers(graph=graph, agentSet=agent_set)

        agentSet_matrix = {}
        copy_graph = copy.deepcopy(graph)
        for node in agentSet_connects.keys():
            agentSet_matrix[node] = []

        while copy_graph[source] != {}:
            source_set = copy_graph[source]
            node_list = list(source_set.keys())
            min_edge = min(list(source_set.values()))
            for node in node_list:

                # initial algorithm
                # if source_set[node] <= agentSet_connects[node]:
                #     agentSet_matrix[node].append(source_set[node])
                #     del copy_graph[source][node]
                #     del copy_graph[node]
                # elif source_set[node] > agentSet_connects[node]:
                #     agentSet_matrix[node].append(agentSet_connects[node])
                #     copy_graph[source][node] -= agentSet_connects[node]

                # second algorithm for layering
                if source_set[node] != min_edge:
                    source_set[node] -= min_edge
                else:
                    del source_set[node]
                agentSet_matrix[node].append(min_edge)

        agentSet_matrix, max_len = self.convert_layer_matrix(agentSet_matrix)
        self.layering_graph = self.create_new_layers_graph(graph, source, agentSet_matrix, max_len)

    def expanding(self, layering_graph, source):
        self.init_string_dic()
        for node in layering_graph.keys():
            source_set = list(layering_graph[node]['adj'][source].keys())
            for each_agent in source_set:
                if layering_graph[node]['adj'][source][each_agent] > 1:
                    num = layering_graph[node]['adj'][source][each_agent]
                    counter = num - 1
                    while counter > 0:
                        s = self.check_which_to_use()
                        layering_graph[node]['adj'][source][each_agent + s] = 1
                        layering_graph[node]['adj'][each_agent + s] = copy.deepcopy(
                            layering_graph[node]['adj'][each_agent])
                        counter -= 1
                    layering_graph[node]['adj'][source][each_agent] = 1
        return layering_graph

    def PP_FFA(self, expanded_graph, objP, objO, distinct=False):
        counter = 0
        result = {}
        for node in expanded_graph.keys():
            start = time.time()
            result[node] = {}
            result[node]['re'] = []
            result[node]['m'] = expanded_graph[node]['number']
            if not distinct:
                graph = Bipartite(graph=expanded_graph[node]['adj'], directed=True, permutation=False, allow_multitask=True,
                                  sink=self.sink,
                                  source=self.source,
                                  objp=objP,
                                  objo=objO)
                graph.execute()
                single_result = graph.result

                # f = open("all_expand_single_result.txt", "w")
                # for _node in single_result.keys():
                #     s = str(_node) + ": " + str(single_result[_node])
                #     f.write(f"{s}\n")
                # f.close()

                final_result = graph.generate_results(single_result, agentSet=graph.agent_set)
                logging.info(f"{len(graph.agent_set)} * {len(graph.object_set)} - {counter + 1} - {time.time() - start}")
                # graph = test()
                # graph.test_fun()
                # pprint.pprint(graph.result)

                result[node]['re'] += final_result

            else:
                pre_graph = copy.deepcopy(expanded_graph[node]['adj'])
                expanded_graph[node]['re'] = []
                while expanded_graph[node]['number'] > 0:
                    graph = Bipartite(graph=expanded_graph[node]['adj'], directed=True, permutation=False,
                                      allow_multitask=True,
                                      sink=self.sink,
                                      source=self.source,
                                      objp=objP,
                                      objo=objO)
                    graph.execute()
                    single_result = graph.result
                    final_result = graph.generate_results(single_result, agentSet=graph.agent_set)

                    expanded_graph[node]['re'] += final_result
                    expanded_graph[node]['adj'] = self.modifiy_distinc(pre_graph, final_result)
                    pre_graph = copy.deepcopy(expanded_graph[node]['adj'])
                    expanded_graph[node]['number'] -= 1
                    logging.info(f"{len(graph.agent_set)} * {len(graph.object_set)} - {self.check_edge_number(expanded_graph[node]['adj'], graph.agent_set)}- {counter + 1} - {time.time() - start}")

                result[node]['m'] = 1
                result[node]['re'] = expanded_graph[node]['re']
            counter += 1







        return result


    def par_PP_FFA(self, i, expanded_graph, objP, objO):
        start = time.time()
        graph = Bipartite(graph=expanded_graph, directed=True, permutation=False, allow_multitask=True,
                          sink=self.sink,
                          source=self.source,
                          objp=objP,
                          objo=objO)
        graph.execute()
        # graph = test()
        # graph.test_fun()
        logging.info(f"{i} - {time.time() - start}")
        return graph.result

    def merge(self):
        pass

    def create_new_layers_graph(self, graph, source, number_layer, max_len):
        layer_graph = {}
        for i in range(1, max_len + 1):
            current = []
            for node in number_layer.keys():
                current.append(number_layer[node][i - 1])
            current = np.array(current)
            non_zero_index = np.nonzero(current)[0]
            if sum(current) / len(non_zero_index) == current[non_zero_index[0]]:
                layer_graph[str(i)] = {}
                layer_graph[str(i)]['number'] = current[non_zero_index[0]]
                layer_graph[str(i)]['adj'] = copy.deepcopy(graph)
                for node in number_layer.keys():
                    if number_layer[node][i - 1] != 0:
                        layer_graph[str(i)]['adj'][source][node] = 1
                    else:
                        del layer_graph[str(i)]['adj'][source][node]
                        del layer_graph[str(i)]['adj'][node]

        return layer_graph

    def convert_layer_matrix(self, number_layer):
        max_len = 0
        for node in number_layer.keys():
            if len(number_layer[node]) > max_len:
                max_len = len(number_layer[node])
        for node in number_layer.keys():
            if len(number_layer[node]) < max_len:
                number_layer[node] += [0] * (max_len - len(number_layer[node]))
        return number_layer, max_len

    def init_string_dic(self):
        s = string.printable
        for i in range(len(s) - 1):
            self.string_dic[s[i]] = s[i + 1]
        self.string_dic[s[-1]] = s[0]

    def check_which_to_use(self):
        l = string.printable[-1]
        if self.used_dic == {}:
            s = string.printable[0]
            self.used_dic[s] = 1
            return s
        last_use = list(self.used_dic.keys())[-1]
        counter = 0
        for i in range(len(last_use)):
            if last_use[i] == l:
                counter += 1
        if counter == len(last_use):
            s = string.printable[0] * (len(last_use) + 1)
            self.used_dic[s] = 1
            return s
        else:
            index = len(last_use) - counter - 1
            s = ''
            for i in range(len(last_use)):
                if i < index:
                    s += last_use[i]
                else:
                    s += self.string_dic[last_use[i]]
            self.used_dic[s] = 1
            return s

    def modifiy_distinc(self, graph, pre_result):
        for pair in pre_result:
            if pair[1] in graph[pair[0]]:
                del graph[pair[0]][pair[1]]
        return copy.deepcopy(graph)

    def check_edge_number(self, graph, agenset):
        count = 0
        for node in agenset:
            count += len(list(graph[node].keys()))
        return count


if __name__ == "__main__":
    pass
