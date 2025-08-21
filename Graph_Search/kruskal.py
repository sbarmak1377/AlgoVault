from typing import Any, Dict, List, Tuple
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

class DisjointSet:
    def __init__(self):
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
    def find(self, x: Any) -> Any:
        if self.parent.get(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        else:
            self.parent.setdefault(x, x)
        self.rank.setdefault(x, 0)
        return self.parent[x]
    def union(self, a: Any, b: Any) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: 
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def kruskal_mst(graph: Graph) -> List[Tuple[Any, Any, float]]:
    if graph.directed:
        raise ValueError("Kruskal's MST is defined for undirected (symmetric) graphs.")
    ds = DisjointSet()
    for u in graph.nodes(): ds.find(u)
    edges = sorted(graph.edges(), key=lambda e: e[2])
    out: List[Tuple[Any, Any, float]] = []
    for u, v, w in edges:
        if ds.union(u, v):
            out.append((u, v, w))
    return out

def main():
    print("=== Kruskal on symmetric graph ===")
    g = sample_symmetric_graph()
    print(kruskal_mst(g))
    print("=== Kruskal on directed graph (should raise) ===")
    try:
        d = sample_directed_graph_general()
        print(kruskal_mst(d))
    except Exception as e:
        print("Not applicable:", e)

if __name__ == "__main__":
    main()
