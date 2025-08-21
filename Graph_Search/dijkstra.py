from typing import Any, Dict, Optional, Set, Tuple, List
import heapq
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

INF = float("inf")

def dijkstra(graph: Graph, source: Any) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    dist: Dict[Any, float] = {u: INF for u in graph.nodes()}
    parent: Dict[Any, Optional[Any]] = {u: None for u in graph.nodes()}
    dist[source] = 0.0
    pq: List[Tuple[float, Any]] = [(0.0, source)]
    visited: Set[Any] = set()
    while pq:
        du, u = heapq.heappop(pq)
        if u in visited: 
            continue
        visited.add(u)
        for v, w in graph.neighbors(u).items():
            if w < 0:
                raise ValueError("Dijkstra requires non-negative weights.")
            alt = du + w
            if alt < dist[v]:
                dist[v] = alt; parent[v] = u; heapq.heappush(pq, (alt, v))
    return dist, parent

def main():
    print("=== Dijkstra on symmetric graph ===")
    g = sample_symmetric_graph()
    print(dijkstra(g, "A")[0])

    print("=== Dijkstra on directed graph ===")
    d = sample_directed_graph_general()
    print(dijkstra(d, "A")[0])

if __name__ == "__main__":
    main()
