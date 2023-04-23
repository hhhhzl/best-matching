import pprint
import random
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK


def Sort_Tuple(tup):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key=lambda x: x[-1])
    return tup


def auto_generate_graph_one(agent, object):
    m = 0
    graph = {DEFAULT_SOURCE: {}}
    agentSet = [str(i) for i in range(1, agent + 1)]
    objectSet = [str(i) for i in range(agent + 1, agent + object + 1)]
    for each_agent in agentSet:
        graph[DEFAULT_SOURCE][each_agent] = 1
        number_threshold = random.randint(1, object)
        number_connect = random.randint(1, number_threshold)
        graph[each_agent] = {}
        while number_connect >= 0:
            x = random.randint(agent + 1, agent + object)
            graph[each_agent][str(x)] = 1
            m += 1
            number_connect -= 1
    for each_object in objectSet:
        graph[each_object] = {}
        graph[each_object][DEFAULT_SINK] = 1
    graph[DEFAULT_SINK] = {}
    return graph, agentSet, objectSet, m


def auto_generate_graph_one_s(agent, object):
    m = 0
    graph = {DEFAULT_SOURCE: {}}
    agentSet = [str(i) for i in range(1, agent + 1)]
    objectSet = [str(i) for i in range(agent + 1, agent + object + 1)]
    for each_agent in agentSet:
        graph[DEFAULT_SOURCE][each_agent] = 1
        number_threshold = random.randint(1, object)
        number_connect = random.randint(1, number_threshold)
        graph[each_agent] = {}
        while number_connect >= 0:
            x = random.randint(agent + 1, agent + object)
            graph[each_agent][str(x)] = 1
            m += 1
            number_connect -= 1
    for each_object in objectSet:
        graph[each_object] = {}
        graph[each_object][DEFAULT_SINK] = 1
    graph[DEFAULT_SINK] = {}
    return graph, agentSet, objectSet, m


def auto_generate_graph(agent, object, max_unit):
    m = 0
    graph = {DEFAULT_SOURCE: {}}
    agentSet = [str(i) for i in range(1, agent + 1)]
    objectSet = [str(i) for i in range(agent + 1, agent + object + 1)]
    for each_agent in agentSet:
        graph[DEFAULT_SOURCE][each_agent] = random.randint(3, max_unit)
        # graph[DEFAULT_SOURCE][each_agent] = 1
        number_threshold = random.randint(1, object)
        number_connect = random.randint(1, number_threshold)
        graph[each_agent] = {}
        while number_connect >= 0:
            x = random.randint(agent + 1, agent + object)
            graph[each_agent][str(x)] = 1
            m += 1
            number_connect -= 1
    for each_object in objectSet:
        graph[each_object] = {}
        graph[each_object][DEFAULT_SINK] = 1
    graph[DEFAULT_SINK] = {}
    return graph, agentSet, objectSet, m


def re_order_tuple_list(l1, node):
    try:
        current = l1[node]
        init = node + 1
        pres = l1[:node][:]
        if node < len(l1) - 1:
            while (node + 1 < len(l1)) and current[1] >= l1[node + 1][1]:
                node += 1
            pres += l1[init:node + 1][:]
            pres.append(current)
            pres += l1[node + 1:][:]
        else:
            pres.append(current)
        return pres
    except:
        print("Wrong Index")


if __name__ == "__main__":
    gen = [('6', 4.1), ('5', 4.1)]
    print(re_order_tuple_list(gen, 0))
