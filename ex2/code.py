"""Second exercise."""
import heapq

from logger import logger


def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    parent = {node: None for node in graph}

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

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    if path[0] == start:
        return path
    return []

def run(config):
    graph = config.get("weighted_graph", {})
    if not graph:
        logger.error("Aucun graphe fourni dans la config.")
        return
    logger.info("Dijkstra depuis A :")
    dist, parent = dijkstra(graph, "A")
    for node in graph:
        path = reconstruct_path(parent, "A", node)
        if path:
            logger.info(f"Chemin vers {node} : {' -> '.join(path)} (distance : {dist[node]})")
        else:
            logger.info(f"Aucun chemin vers {node}")
