from typing import Any, Dict, List, Optional, Set, Tuple
from collections import deque
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

def bfs(graph: Graph, source: Any) -> Tuple[List[Any], Dict[Any, Optional[Any]], Dict[Any, int]]:
    visited: Set[Any] = set([source])
    parent: Dict[Any, Optional[Any]] = {source: None}
    dist: Dict[Any, int] = {source: 0}
    order: List[Any] = []
    q = deque([source])
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph.neighbors(u).keys():
            if v not in visited:
                visited.add(v); parent[v] = u; dist[v] = dist[u] + 1; q.append(v)
    return order, parent, dist

def main():
    print("=== BFS on symmetric graph ===")
    g = sample_symmetric_graph()
    print(bfs(g, "A")[0])

    print("=== BFS on directed graph ===")
    d = sample_directed_graph_general()
    print(bfs(d, "A")[0])

if __name__ == "__main__":
    main()
