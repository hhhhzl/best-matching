import pprint
import random
from configs.AssignNet_config import DEFAULT_SOURCE, DEFAULT_SINK


def Sort_Tuple(tup):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key=lambda x: x[-1])
    return tup


def auto_generate_graph(agent, object, max_unit):
    m = 0
    graph = {DEFAULT_SOURCE: {}}
    agentSet = [str(i) for i in range(1, agent + 1)]
    objectSet = [str(i) for i in range(agent + 1, agent + object + 1)]
    for each_agent in agentSet:
        graph[DEFAULT_SOURCE][each_agent] = random.randint(1, max_unit)
        # graph[DEFAULT_SOURCE][each_agent] = 1
        number_connect = random.randint(1, object)
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


if __name__ == "__main__":
    graph = auto_generate_graph(10, 10)
    pprint.pprint(graph)
