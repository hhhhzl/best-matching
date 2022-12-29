import concurrent.futures
from AssignNet.transportation_problem.basic import Trans_Problem
from tools import auto_generate_graph
import time
import pprint
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK
import copy
from joblib import Parallel, delayed

if __name__ == "__main__":
    generated_graph, agent_set = auto_generate_graph(2000, 2000)
    generated_graph_copy = copy.deepcopy(generated_graph)
    # # 全部展开
    # graph = {'1': {}}
    # graph['1']['adj'] = generated_graph
    # run = Trans_Problem()
    # G = run.expanding(layering_graph=graph, source=DEFAULT_SOURCE)
    # start = time.time()
    # run.PP_FFA(G)
    # print('全部展开时间：', time.time() - start)

    # 分层展开，no par
    start = time.time()
    new = Trans_Problem()
    new.layering(generated_graph_copy, DEFAULT_SOURCE, agent_set)
    graph1 = new.layering_graph
    G1 = new.expanding(layering_graph=graph1, source=DEFAULT_SOURCE)
    G2 = copy.deepcopy(G1)
    print('分层展开无进程运算开始：', time.time() - start)
    start = time.time()
    print(list(G1.keys()))
    new.PP_FFA(G1)
    print('分层展开无进程：', time.time() - start)


    # par

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     nodes = list(G2.keys())
    #     results = [executor.submit(new.par_PP_FFA, G2[node]['adj']) for node in nodes]
    #     start1 = time.time()
    #     for f in concurrent.futures.as_completed(results):
    #         # pprint.pprint(f.result())
    #         pass
    # # nodes = list(G2.keys())
    # # Parallel(n_jobs=2)(delayed(new.par_PP_FFA)(G2[node]['adj']) for node in nodes)
    # print('分层展开使用进程：', time.time() - start1)