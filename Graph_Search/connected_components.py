from typing import Any, List, Set
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

def connected_components(graph: Graph) -> List[Set[Any]]:
    seen: Set[Any] = set()
    comps: List[Set[Any]] = []
    for start in graph.nodes():
        if start in seen: 
            continue
        comp: Set[Any] = set()
        stack = [start]; seen.add(start)
        while stack:
            u = stack.pop()
            comp.add(u)
            it = graph.undirected_view_neighbors(u) if graph.directed else graph.neighbors(u).items()
            for v, _ in it:
                if v not in seen:
                    seen.add(v); stack.append(v)
        comps.append(comp)
    return comps

def main():
    print("=== Components on symmetric graph ===")
    g = sample_symmetric_graph()
    print(connected_components(g))

    print("=== Weak components on directed graph ===")
    d = sample_directed_graph_general()
    print(connected_components(d))

if __name__ == "__main__":
    main()
