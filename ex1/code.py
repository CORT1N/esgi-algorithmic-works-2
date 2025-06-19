"""First exercise."""
from collections import deque

from logger import logger


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    logger.info(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            logger.info(f"BFS visit: {node}")
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

def has_cycle_dfs(graph) -> bool:
    visited = set()
    rec_stack = set()

    def dfs_cycle(node) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    return any(node not in visited and dfs_cycle(node) for node in graph)

def connected_components_bfs(graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            queue = deque([node])
            component = []

            while queue:
                current = queue.popleft()
                if current not in visited:
                    visited.add(current)
                    component.append(current)
                    for neighbor in graph.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)

            components.append(component)

    return components

def run(config):
    graph = config.get("graph", {})
    if not graph:
        logger.error("Aucun graphe fourni dans la config.")
        return
    logger.info("Parcours DFS récursif depuis A :")
    dfs(graph, "A")
    logger.info("Parcours BFS depuis A :")
    bfs(graph, "A")
    logger.info("Détection de cycles (DFS) :")
    if has_cycle_dfs(graph):
        logger.info("Cycle détecté dans le graphe.")
    else:
        logger.info("Aucun cycle détecté.")
    logger.info("Composantes connexes (BFS) : ")
    components = connected_components_bfs(graph)
    for idx, comp in enumerate(components, 1):
        logger.info(f" Composante {idx} : {comp}")
