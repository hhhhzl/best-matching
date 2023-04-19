from tools import auto_generate_graph_one_s
import time
import pprint
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import copy
import logging
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
from AssignNet.bipartite_matching.basic import Bipartite

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def data_generate(number):
    generated_graph, agent_set, object_set, m = auto_generate_graph_one_s(number, number)
    return generated_graph, agent_set, object_set, m


def percent_cal(agent_set, object_set, result, method):
    appearance = {}
    total = {}
    for i in agent_set:
        total[i] = 0
    for i in object_set:
        total[i] = 0

    for each_pair in result:
        if each_pair[0] not in appearance:
            appearance[each_pair[0]] = 1
        else:
            appearance[each_pair[0]] += 1
        if each_pair[1] not in appearance:
            appearance[each_pair[1]] = 1
        else:
            appearance[each_pair[1]] += 1

        total[each_pair[0]] = 1
        total[each_pair[1]] = 1

    percentage = sum(total.values()) / len(list(total.keys()))
    logging.info(f'{method}分配率: {percentage}')


def test_PFFA(graph, agent_set, object_set, number, m):
    operate_graph = copy.deepcopy(graph)
    start = time.time()
    _graph = Bipartite(graph=operate_graph, directed=True, permutation=True, allow_multitask=False)
    _graph.execute()
    result = _graph.result
    final_result = _graph.generate_results(result, agentSet=agent_set)
    percent_cal(agent_set, object_set, final_result, "PFFA")
    logging.info(f'{number} * {number} - {m} - 时间运算：{"{:.3f}".format(time.time() - start)}s')
    return final_result


def test_FFA(graph, agent_set, object_set, number, m):
    operate_graph = copy.deepcopy(graph)
    start = time.time()
    _graph = Bipartite(graph=operate_graph, directed=True, permutation=False, allow_multitask=False)
    _graph.execute()
    result = _graph.result
    final_result = _graph.generate_results(result, agentSet=agent_set)
    percent_cal(agent_set, object_set, final_result, "FFA")
    logging.info(f'{number} * {number} - {m} - 时间运算：{"{:.3f}".format(time.time() - start)}s')
    return final_result


def main():
    for (item, number) in enumerate([2500]):
        for i in range(5):
            logging.info(f'TP测试{number} - {i + 1}开始')
            generated_graph, agent_set, object_set, m = data_generate(number)
            result = test_FFA(generated_graph, agent_set, object_set, number, m)
            result = test_PFFA(generated_graph, agent_set, object_set, number, m)


if __name__ == "__main__":
    logging.info(f'TP测试开始')
    main()
    logging.info(f'TP测试结束')
