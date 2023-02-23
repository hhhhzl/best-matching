import concurrent.futures
from AssignNet.transportation_problem.basic import Trans_Problem
from tools import auto_generate_graph
import time
import pprint
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import copy
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Pool, cpu_count
from multiprocessing import Queue
from multiprocessing import Lock
from multiprocessing import Pipe
import logging
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
from concurrent.futures import ProcessPoolExecutor
import asyncio
from functools import partial
import pandas as pd
import random

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def data_generate(agentSet, objectSet):
    m = 0
    graph = {DEFAULT_SOURCE: {}}
    counter = 1
    agent_index = {}
    index_agent = {}
    object_index = {}
    index_object = {}
    agent_Set = []
    object_Set = []

    for agent in agentSet.keys():
        agent_Set.append(str(counter))
        agent_index[agent] = str(counter)
        index_agent[str(counter)] = agent
        counter += 1

    for object in objectSet.keys():
        object_Set.append(str(counter))
        object_index[object] = str(counter)
        index_object[str(counter)] = object
        counter += 1

    for each_agent in agent_Set:
        # graph[DEFAULT_SOURCE][each_agent] = random.choice([3, 5])
        graph[DEFAULT_SOURCE][each_agent] = 3
        graph[each_agent] = {}
        for obj in agentSet[index_agent[each_agent]]:
            graph[each_agent][str(object_index[str(obj)])] = 1
            m += 1

    for each_object in object_Set:
        graph[each_object] = {}
        graph[each_object][DEFAULT_SINK] = 1
    graph[DEFAULT_SINK] = {}
    return graph, agent_Set, object_Set, m, agent_index, index_agent, object_index, index_object


def test_all_expand(generated_graph, number, m):
    operate_graph = copy.deepcopy(generated_graph)
    graph = copy.deepcopy({'1': {}})
    graph['1']['adj'] = operate_graph
    start = time.time()
    run = Trans_Problem()
    G = run.expanding(layering_graph=graph, source=DEFAULT_SOURCE)
    logging.info(f'层数：- {len(list(G.keys()))}层')
    run.PP_FFA(copy.deepcopy(G))
    logging.info(f'{number} * {number}- {m} - 全部展开时间运算：{"{:.3f}".format(time.time() - start)}s')


def test_layering_single_thread(generated_graph, agent_set, object_set, number, _number, m):
    operate_graph = copy.deepcopy(generated_graph)
    g = PFF_SOLVER()
    start = time.time()
    operate_graph1, objectPrice, objectOrder = g.permutation(graph=operate_graph, agentSet=agent_set,
                                                             objectSet=object_set, source=DEFAULT_SOURCE, sink=DEFAULT_SINK)
    logging.info(f'{number} * {_number} - {m} - 排列运算：{"{:.3f}".format(time.time() - start)}s')

    new = Trans_Problem(sink=DEFAULT_SINK, source=DEFAULT_SOURCE)
    new.layering(operate_graph1, DEFAULT_SOURCE, agent_set)
    logging.info(f'{number} * {_number} - {m} - 分层运算：{"{:.3f}".format(time.time() - start)}s')

    graph1 = new.layering_graph
    # graph1 = new.expanding(layering_graph=graph1, source=DEFAULT_SOURCE)

    logging.info(f'层数：- {len(list(graph1.keys()))}层')
    # logging.info(f'{number} * {number} - {m} - 展开运算：{"{:.3f}".format(time.time() - start)}s')
    result = new.PP_FFA(graph1, objectPrice, objectOrder, distinct=True)
    logging.info(f'{number} * {_number} - {m} - 分层展开单进程时间运算：{"{:.3f}".format(time.time() - start)}s')
    return result


def test_layering_multi_thread(generated_graph, agent_set, object_set, number, _number, m):
    operate_graph = copy.deepcopy(generated_graph)
    g = PFF_SOLVER()
    start = time.time()
    operate_graph1, objectPrice, objectOrder = g.permutation(graph=operate_graph, agentSet=agent_set,
                                                             objectSet=object_set, source=DEFAULT_SOURCE, sink=DEFAULT_SINK)
    logging.info(f'{number} * {_number} - {m} - 排列运算：{"{:.3f}".format(time.time() - start)}s')

    new = Trans_Problem()
    new.layering(operate_graph1, DEFAULT_SOURCE, agent_set)
    logging.info(f'{number} * {_number} - {m}- 分层运算：{"{:.3f}".format(time.time() - start)}s')
    graph1 = new.layering_graph

    # graph1 = new.expanding(layering_graph=graph1, source=DEFAULT_SOURCE)
    # logging.info(f'{number} * {number} - {m} - 展开运算：{"{:.3f}".format(time.time() - start)}s')
    #
    graphs = [copy.deepcopy(graph1[node]['adj']) for node in list(graph1.keys())]
    logging.info(f'层数：- {len(graphs)}层')
    result = par(new, graphs, objectPrice, objectOrder)
    logging.info(f'{number} * {_number} - 分层展开时间多进程运算：{"{:.3f}".format(time.time() - start)}s')
    return result


def par(Class, graphs, objP, objO):
    n = len(graphs)
    pool = Pool(processes=multiprocessing.cpu_count())
    result = []
    for i in range(n):
        result.append(pool.apply_async(func=Class.par_PP_FFA, args=(i, graphs[i], objP, objO)))
    pool.close()
    pool.join()
    ans = [res.get() for res in result]
    return ans


def main():
    data = pd.read_csv("ALL_EXPAND_MATCHING_E.csv")
    agentSet = {}
    objectSet = {}
    for index, row in data.iterrows():
        l1 = str(row['改题专家']).split(', ')
        if row['GQ_ID'] not in agentSet:
            agentSet[str(row['GQ_ID'])] = l1
        for i in l1:
            if str(i) not in objectSet:
                objectSet[str(i)] = 1

    graph, agent_Set, object_Set, m, agent_index, index_agent, object_index, index_object = data_generate(agentSet,
                                                                                                          objectSet)
    result = test_layering_single_thread(graph, agent_Set, object_Set, len(agent_Set), len(object_Set), m)

    f = open("all_expand_result.txt", "w")
    #
    for each_layer in result.keys():
        layer_number = result[each_layer]['m']
        print(len(result[each_layer]['re']))
        for i in range(layer_number):
            for each_pair in result[each_layer]['re']:
                f.write(f"{index_agent[each_pair[0]]}, {index_object[each_pair[1]]}\n")
    f.close()


def test_non_main():
    data = pd.read_csv("NON_EXPANDING_MATCHING.csv")
    agentSet = {}
    objectSet = {}
    for index, row in data.iterrows():
        # if str(row['改题专家']) != '24':
            l1 = str(row['改题专家']).split(', ')
            if row['QUES_ID'] not in agentSet:
                agentSet[str(row['QUES_ID'])] = l1
            for i in l1:
                if str(i) not in objectSet:
                    objectSet[str(i)] = 1

    graph, agent_Set, object_Set, m, agent_index, index_agent, object_index, index_object = data_generate(agentSet, objectSet)
    result = test_layering_single_thread(graph, agent_Set, object_Set, len(agent_Set), len(object_Set), m)

    f = open("all_expand_result.txt", "w")
    #
    for each_layer in result.keys():
        layer_number = result[each_layer]['m']
        print(len(result[each_layer]['re']))
        for i in range(layer_number):
            for each_pair in result[each_layer]['re']:
                f.write(f"{index_agent[each_pair[0]]}, {index_object[each_pair[1]]}\n")
    f.close()


if __name__ == "__main__":
    logging.info(f'TP测试开始')
    test_non_main()
    logging.info(f'TP测试结束')
