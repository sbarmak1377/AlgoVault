from typing import Any, List, Set, Tuple
import heapq
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

def prim_mst(graph: Graph) -> List[Tuple[Any, Any, float]]:
    if graph.directed:
        raise ValueError("Prim's MST is defined for undirected (symmetric) graphs.")
    nodes = graph.nodes()
    if not nodes: 
        return []
    visited: Set[Any] = set()
    pq: List[Tuple[float, Any, Any]] = []
    out: List[Tuple[Any, Any, float]] = []
    def add(u: Any):
        visited.add(u)
        for v, w in graph.neighbors(u).items():
            if v not in visited:
                heapq.heappush(pq, (w, u, v))
    for root in nodes:
        if root in visited: 
            continue
        add(root)
        while pq:
            w, u, v = heapq.heappop(pq)
            if v in visited: 
                continue
            out.append((u, v, w))
            add(v)
    return out

def main():
    print("=== Prim on symmetric graph ===")
    g = sample_symmetric_graph()
    print(prim_mst(g))
    print("=== Prim on directed graph (should raise) ===")
    try:
        d = sample_directed_graph_general()
        print(prim_mst(d))
    except Exception as e:
        print("Not applicable:", e)

if __name__ == "__main__":
    main()
