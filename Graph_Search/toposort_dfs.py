from typing import Any, Dict, List
from graph_base import Graph
from common_utils import sample_directed_graph_acyclic, sample_symmetric_graph

def toposort_dfs(graph: Graph) -> List[Any]:
    if not graph.directed:
        raise ValueError("Topological sort is defined for directed acyclic graphs only.")
    visited: Dict[Any, int] = {}
    order: List[Any] = []
    def visit(u: Any) -> None:
        state = visited.get(u, 0)
        if state == 1:
            raise ValueError("Cycle detected")
        if state == 2:
            return
        visited[u] = 1
        for v in graph.neighbors(u).keys():
            visit(v)
        visited[u] = 2
        order.append(u)
    for u in graph.nodes():
        if visited.get(u, 0) == 0:
            visit(u)
    order.reverse()
    return order

def main():
    print("=== DFS Topo on directed DAG ===")
    dag = sample_directed_graph_acyclic()
    print(toposort_dfs(dag))
    print("=== DFS Topo on symmetric graph (should raise) ===")
    try:
        g = sample_symmetric_graph()
        print(toposort_dfs(g))
    except Exception as e:
        print("Not applicable:", e)

if __name__ == "__main__":
    main()
