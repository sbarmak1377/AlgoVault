from typing import Any, Dict, List, Optional, Set, Tuple
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

def dfs(graph: Graph, source: Any) -> Tuple[List[Any], Dict[Any, Optional[Any]]]:
    visited: Set[Any] = set()
    parent: Dict[Any, Optional[Any]] = {source: None}
    order: List[Any] = []
    stack: List[Tuple[Any, Optional[Any], bool]] = [(source, None, False)]
    while stack:
        u, p, expanded = stack.pop()
        if not expanded:
            if u in visited: continue
            visited.add(u); parent[u] = p
            stack.append((u, p, True))
            for v in graph.neighbors(u).keys():
                if v not in visited:
                    stack.append((v, u, False))
        else:
            order.append(u)
    return order, parent

def main():
    print("=== DFS on symmetric graph ===")
    g = sample_symmetric_graph()
    print(dfs(g, "A")[0])

    print("=== DFS on directed graph ===")
    d = sample_directed_graph_general()
    print(dfs(d, "A")[0])

if __name__ == "__main__":
    main()
