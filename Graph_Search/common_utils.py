from graph_base import Graph

def sample_symmetric_graph():
    g = Graph(directed=False)
    g.add_edges_from([
        ("A","B",4), ("A","C",2), ("B","C",1), ("B","D",5), ("C","D",8),
        ("C","E",10), ("D","E",2), ("D","Z",6), ("E","Z",3)
    ])
    return g

def sample_directed_graph_acyclic():
    h = Graph(directed=True)
    h.add_edges_from([("cook","eat",1), ("shop","cook",1), ("plan","shop",1), ("plan","cook",1)])
    return h

def sample_directed_graph_general():
    d = Graph(directed=True)
    d.add_edges_from([("A","B",2), ("B","C",5), ("A","C",9), ("C","A",1), ("C","D",3)])
    return d
