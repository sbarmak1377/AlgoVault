from typing import Any, Dict, List
from collections import deque
from graph_base import Graph
from common_utils import sample_directed_graph_acyclic, sample_symmetric_graph

def toposort_kahn(graph: Graph) -> List[Any]:
    if not graph.directed:
        raise ValueError("Topological sort is defined for directed acyclic graphs only.")
    indeg: Dict[Any, int] = {u: 0 for u in graph.nodes()}
    for u, v, _ in graph.edges():
        indeg[v] += 1
    q = deque([u for u, d in indeg.items() if d == 0])
    order: List[Any] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph.neighbors(u).keys():
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(indeg):
        raise ValueError("Graph has at least one cycle; order does not exist.")
    return order

def main():
    print("=== Kahn on directed DAG ===")
    dag = sample_directed_graph_acyclic()
    print(toposort_kahn(dag))
    print("=== Kahn on symmetric graph (should raise) ===")
    try:
        g = sample_symmetric_graph()
        print(toposort_kahn(g))
    except Exception as e:
        print("Not applicable:", e)

if __name__ == "__main__":
    main()
