from tools import auto_generate_graph_one
import time
import pprint
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import copy
import logging
import random
from Algorithms.permutatiion_FF.solver import PFF_SOLVER
from AssignNet.bipartite_matching.basic import Bipartite
import numpy as np

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def data_generate(number):
    agent_number = random.randint(number // 5 * 3, number)
    object_number = number - agent_number
    generated_graph, agent_set, object_set, m = auto_generate_graph_one(agent_number, object_number)
    return generated_graph, agent_set, object_set, m, agent_number, object_number


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

    listr = []
    for value in appearance.keys():
        if value in object_set:
            listr.append(appearance[value])
    # pprint.pprint(listr)
    std = np.std(listr)
    mean = np.mean(listr)
    logging.info(f'{method}方差: {std}')
    return mean, std


def test_PFFA(graph, agent_set, object_set, number, m, agent_number, object_number):
    operate_graph = copy.deepcopy(graph)
    start = time.time()
    _graph = Bipartite(graph=operate_graph, directed=True, permutation=True, allow_multitask=True)
    _graph.execute()
    result = _graph.result
    final_result = _graph.generate_results(result, agentSet=agent_set)
    mean, std = percent_cal(agent_set, object_set, final_result, "PFFA")
    logging.info(f'{number} - {agent_number} * {object_number} - {m} - 时间运算：{"{:.3f}".format(time.time() - start)}s')
    return final_result, mean, std


def test_FFA(graph, agent_set, object_set, number, m, agent_number, object_number):
    operate_graph = copy.deepcopy(graph)
    start = time.time()
    _graph = Bipartite(graph=operate_graph, directed=True, permutation=False, allow_multitask=True)
    _graph.execute()
    result = _graph.result
    final_result = _graph.generate_results(result, agentSet=agent_set)
    mean, std = percent_cal(agent_set, object_set, final_result, "FFA")
    logging.info(f'{number} - {agent_number} * {object_number} - {m} - 时间运算：{"{:.3f}".format(time.time() - start)}s')
    return final_result, mean, std


def main():
    for (item, number) in enumerate([50, 100, 200, 500, 1000]):
        ffa_mean = []
        pffa_mean = []
        ffa_std = []
        pffa_std = []
        for i in range(10):
            logging.info(f'TP测试{number} - {i + 1}开始')
            generated_graph, agent_set, object_set, m, agent_number, object_number = data_generate(number)
            result, mean, std = test_FFA(generated_graph, agent_set, object_set, number, m, agent_number, object_number)
            ffa_mean.append(mean)
            ffa_std.append(std)
            result, mean, std = test_PFFA(generated_graph, agent_set, object_set, number, m, agent_number, object_number)
            pffa_mean.append(mean)
            pffa_std.append(std)

        mean_ffa = np.mean(ffa_mean)
        mean_pffa = np.mean(pffa_mean)
        mean_std_ffa = np.mean(ffa_std)
        mean_std_pffa = np.mean(pffa_std)
        logging.info(f'{mean_ffa} - {mean_pffa} - {mean_std_ffa} - {mean_std_pffa}')


if __name__ == "__main__":
    logging.info(f'TP测试开始')
    main()
    logging.info(f'TP测试结束')
