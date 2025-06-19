"""Second exercise."""
from __future__ import annotations

import heapq

from logger import logger


def dijkstra(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    ) -> tuple[dict[str, float], dict[str, str | None]]:
    """Dijkstra's algorithm for finding the shortest paths from a start node."""
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    parent = dict.fromkeys(graph, None)

    heap = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)
        if current_dist > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                parent[neighbor] = node
                heapq.heappush(heap, (distance, neighbor))

    return dist, parent

def reconstruct_path(parent: dict[str, str | None], start: str, end: str) -> list[str]:
    """Reconstruct the shortest path from start to end using the parent map."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    if path[0] == start:
        return path
    return []

def run(config: dict) -> None:
    """Run the Dijkstra's algorithm."""
    graph = config.get("weighted_graph", {})
    if not graph:
        logger.error("Aucun graphe fourni dans la config.")
        return
    logger.info("Dijkstra depuis A :")
    dist, parent = dijkstra(graph, "A")
    for node in graph:
        path = reconstruct_path(parent, "A", node)
        if path:
            logger.info(
                f"Chemin vers {node} : {' -> '.join(path)} (distance : {dist[node]})",
                )
        else:
            logger.info(f"Aucun chemin vers {node}")
