"""Third exercise."""
from logger import logger


def bellman_ford(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    parent = {node: None for node in graph}

    nodes = list(graph.keys())

    for _ in range(len(nodes) - 1):
        updated = False
        for u in nodes:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    updated = True
        if not updated:
            break

    for u in nodes:
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                return None, None

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
        logger.error("Aucun graphe pondéré fourni dans la config.")
        return

    start_node = "A"
    logger.info(f"Bellman-Ford depuis {start_node} :")

    dist, parent = bellman_ford(graph, start_node)
    if dist is None:
        logger.error("Cycle de poids négatif détecté dans le graphe !")
        return

    for node in graph:
        path = reconstruct_path(parent, start_node, node)
        if path:
            logger.info(f"Chemin vers {node} : {' -> '.join(path)} (distance : {dist[node]})")
        else:
            logger.info(f"Aucun chemin vers {node}")