def check_bipartite_inputs(graph, sink=None, source=None, directed=None, weighted=None):
    if type(graph) == dict:
        return check_adj_list(graph, sink, source, directed, weighted)
    elif type(graph) == list and type(graph[0]) == tuple and (len(graph[0]) == 2 or len(graph[0]) == 3):
        return check_edges(graph, sink, source, directed, weighted)
    elif type(graph) == list and type(graph[0]) == list:
        # matricx
        return False
    else:
        return False, 'Invalid Graph input type.'


def check_adj_list(graph, sink, source, directed, weighted):
    if graph == {}:
        return False, 'Invalid Graph, Graph empty.'
    else:
        if sink is not None and source is not None and directed is not None and weighted is not None:
            return True, 'Valid.'
        elif sink is None and source is None and directed is not None and weighted is not None:
            return True, 'Valid.'
        else:
            return False, 'Invalid inputs.'


def check_edges(graph, sink, source, directed, weighted):
    counter = len(graph[0])
    for node in graph:
        if node == ():
            return False, 'Invalid Graph, Graph empty.'
        elif len(node) != counter:
            return False, 'Each node should be the same length.'

    if sink is not None and source is not None and directed is not None and (weighted is not None or weighted is None):
        return True, 'Valid.'
    elif sink is None and source is None and directed is not None and (weighted is not None or weighted is None):
        return True, 'Valid.'
    else:
        return False, 'Invalid inputs.'
