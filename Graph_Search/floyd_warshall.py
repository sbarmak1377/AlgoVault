from typing import Any, Dict
from graph_base import Graph
from common_utils import sample_symmetric_graph, sample_directed_graph_general

INF = float("inf")

def floyd_warshall(graph: Graph) -> Dict[Any, Dict[Any, float]]:
    nodes = graph.nodes()
    dist: Dict[Any, Dict[Any, float]] = {u: {v: INF for v in nodes} for u in nodes}
    for u in nodes: dist[u][u] = 0.0
    for u, v, w in graph.edges():
        dist[u][v] = min(dist[u][v], w)
        if not graph.directed:
            dist[v][u] = min(dist[v][u], w)
    for k in nodes:
        for i in nodes:
            dik = dist[i][k]
            if dik == INF: 
                continue
            for j in nodes:
                alt = dik + dist[k][j]
                if alt < dist[i][j]:
                    dist[i][j] = alt
    for u in nodes:
        if dist[u][u] < 0:
            raise ValueError("Negative-weight cycle.")
    return dist

def main():
    print("=== Floyd–Warshall on symmetric graph ===")
    g = sample_symmetric_graph()
    print(floyd_warshall(g)["A"]["Z"])

    print("=== Floyd–Warshall on directed graph ===")
    d = sample_directed_graph_general()
    print(floyd_warshall(d)["A"]["D"])

if __name__ == "__main__":
    main()
