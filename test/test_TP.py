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

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def data_generate(number, max):
    generated_graph, agent_set, object_set, m = auto_generate_graph(number, number, max)
    return generated_graph, agent_set, object_set, m


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


def test_layering_single_thread(generated_graph, agent_set, object_set, number, m):
    operate_graph = copy.deepcopy(generated_graph)
    g = PFF_SOLVER()
    start = time.time()
    operate_graph1 = g.permutation(graph=operate_graph, agentSet=agent_set, objectSet=object_set, source=DEFAULT_SOURCE)
    logging.info(f'{number} * {number} - {m} - 排列运算：{"{:.3f}".format(time.time() - start)}s')
    new = Trans_Problem(sink=DEFAULT_SINK, source=DEFAULT_SOURCE)
    new.layering(operate_graph1, DEFAULT_SOURCE, agent_set)
    logging.info(f'{number} * {number} - {m} - 分层运算：{"{:.3f}".format(time.time() - start)}s')
    graph1 = new.layering_graph
    G1 = new.expanding(layering_graph=graph1, source=DEFAULT_SOURCE)
    logging.info(f'层数：- {len(list(G1.keys()))}层')
    logging.info(f'{number} * {number} - {m} - 展开运算：{"{:.3f}".format(time.time() - start)}s')
    new.PP_FFA(G1)
    logging.info(f'{number} * {number} - {m} - 分层展开时间运算：{"{:.3f}".format(time.time() - start)}s')


def test_layering_multi_thread(generated_graph, agent_set, object_set, number, m):
    operate_graph = copy.deepcopy(generated_graph)
    g = PFF_SOLVER()
    start = time.time()
    operate_graph1 = g.permutation(graph=operate_graph, agentSet=agent_set, objectSet=object_set, source=DEFAULT_SOURCE)
    logging.info(f'{number} * {number} - {m} - 排列运算：{"{:.3f}".format(time.time() - start)}s')

    new = Trans_Problem()
    new.layering(operate_graph1, DEFAULT_SOURCE, agent_set)
    logging.info(f'{number} * {number} - {m}- 分层运算：{"{:.3f}".format(time.time() - start)}s')
    graph1 = new.layering_graph
    G1 = new.expanding(layering_graph=graph1, source=DEFAULT_SOURCE)
    logging.info(f'{number} * {number} - {m} - 展开运算：{"{:.3f}".format(time.time() - start)}s')
    #
    graphs = [copy.deepcopy(G1[node]['adj']) for node in list(G1.keys())]
    logging.info(f'层数：- {len(graphs)}层')
    par(new, graphs)
    logging.info(f'{number} * {number} - 分层展开时间多进程运算：{"{:.3f}".format(time.time() - start)}s')


def par(Class, graphs):
    # loop = asyncio.get_running_loop()
    # lstFutures = []
    # # Create an executor with a maximum of eight workers
    # objExecutor = ProcessPoolExecutor(max_workers=8)
    # # Create eight processes using the executor
    # for _ in graphs:
    #     lstFutures.append(loop.run_in_executor(objExecutor, Class.par_PP_FFA, _))
    # # Wait for all processes to complete
    # await asyncio.wait(lstFutures)
    # n = len(graphs)
    # result = []
    # pool = Pool(processes=multiprocessing.cpu_count())
    # for k in range(n):
    #     p = partial(Class.par_PP_FFA, expanded_graph=graphs[k])
    #     result_list = pool.map(p, range(n))
    #     for result in result_list:
    #         pass
    # pool.close()
    # pool.join()
    n = len(graphs)
    pool = Pool(processes=multiprocessing.cpu_count())
    result = []
    for i in range(n):
        result.append(pool.apply_async(func=Class.par_PP_FFA, args=(i, graphs[i], )))
    pool.close()
    pool.join()
    ans = [res.get() for res in result]

def main():
    for (item, number) in enumerate([10, 100, 200, 300]):
        logging.info(f'TP测试{item + 1}开始')
        generated_graph, agent_set, object_set, m = data_generate(number, 50)
        # test_all_expand(generated_graph, number, m)
        test_layering_single_thread(generated_graph, agent_set, object_set, number, m)
        test_layering_multi_thread(generated_graph, agent_set, object_set,  number, m)
        logging.info(f'TP测试{item + 1}结束')


if __name__ == "__main__":
    logging.info(f'TP测试开始')
    main()
    logging.info(f'TP测试结束')

