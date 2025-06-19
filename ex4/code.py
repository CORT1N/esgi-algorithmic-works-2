"""Fourth exercise."""
from __future__ import annotations

from collections import deque
from copy import deepcopy

from logger import logger


def ford_fulkerson(
    capacity_graph: dict[str, dict[str, int]],
    source: str,
    sink: str,
    ) -> int:
    """Ford-Fulkerson algorithm using DFS to find the maximum flow in a flow network."""
    graph = deepcopy(capacity_graph)
    max_flow = 0

    def dfs(
        path: list[tuple[str, str]],
        visited: set[str],
        node: str,
        ) -> list[tuple[str, str]] | None:
        if node == sink:
            return path
        visited.add(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in visited and graph[node][neighbor] > 0:
                res = dfs([*path, (node, neighbor)], visited, neighbor)
                if res:
                    return res
        return None

    while True:
        visited = set()
        path = dfs([], visited, source)
        if not path:
            break
        flow = min(graph[u][v] for u, v in path)
        for u, v in path:
            graph[u][v] -= flow
            graph[v].setdefault(u, 0)
            graph[v][u] += flow
        max_flow += flow
        logger.info(f"Chemin trouvé : {path} avec flux = {flow}")

    return max_flow


def edmonds_karp(
    capacity_graph: dict[str, dict[str, int]],
    source: str,
    sink: str,
    ) -> int:
    """Edmonds-Karp algorithm using BFS to find the maximum flow in a flow network."""
    graph = deepcopy(capacity_graph)
    max_flow = 0

    while True:
        parent = {}
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in graph.get(u, {}):
                if v not in visited and graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break

        if sink not in parent:
            break

        path = []
        v = sink
        while v != source:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()

        flow = min(graph[u][v] for u, v in path)
        for u, v in path:
            graph[u][v] -= flow
            graph[v].setdefault(u, 0)
            graph[v][u] += flow
        max_flow += flow
        logger.info(f"Chemin trouvé : {path} avec flux = {flow}")

    return max_flow


def run(config: dict) -> None:
    """Run the Ford-Fulkerson and Edmonds-Karp algorithms."""
    graph = config.get("capacity_graph", {})
    if not graph:
        logger.error("Aucun graphe de capacité fourni dans la config.")
        return

    logger.info("Algorithme de Ford-Fulkerson (DFS) :")
    flow_ff = ford_fulkerson(graph, "A", "F")
    logger.info(f"Flux maximal (Ford-Fulkerson) : {flow_ff}")

    logger.info("Algorithme de Edmonds-Karp (BFS)")
    flow_ek = edmonds_karp(graph, "A", "F")
    logger.info(f"Flux maximal (Edmonds-Karp) : {flow_ek}")
