"""Seventh exercise."""
import time
from collections.abc import Sequence
from itertools import permutations
from typing import Any, Callable

from logger import logger


def is_satisfiable(
    clauses: Sequence[Sequence[str]],
    assignment: dict[str, bool],
    ) -> bool:
    """Check if a given assignment satisfies all clauses in a CNF formula."""
    for clause in clauses:
        satisfied = False
        for literal in clause:
            var = literal.strip("-")
            value = assignment.get(var)
            if literal.startswith("-"):
                satisfied |= not value
            else:
                satisfied |= bool(value)
        if not satisfied:
            return False
    return True

def tsp_nearest_neighbor(
    matrix: Sequence[Sequence[float]],
    start: int = 0,
    ) -> tuple[list[int], float]:
    """Approximate solution for the Traveling Salesman Problem."""
    """Using the nearest neighbor heuristic."""
    n = len(matrix)
    visited = [False] * n
    path = [start]
    total_distance = 0
    current = start
    visited[current] = True

    for _ in range(n - 1):
        nearest = None
        min_dist = float("inf")
        for i in range(n):
            if not visited[i] and matrix[current][i] < min_dist:
                nearest = i
                min_dist = matrix[current][i]
        if nearest is not None:
            path.append(nearest)
            total_distance += min_dist
            visited[nearest] = True
            current = nearest

    total_distance += matrix[current][start]
    path.append(start)

    return path, total_distance

def tsp_brute_force(matrix: Sequence[Sequence[float]]) -> tuple[list[int], float]:
    """Exact solution for the Traveling Salesman Problem using brute force."""
    n = len(matrix)
    cities = list(range(n))
    min_distance = float("inf")
    best_path = []

    for perm in permutations(cities[1:]):
        path = [0, *list(perm), 0]
        distance = sum(matrix[path[i]][path[i+1]] for i in range(n))
        if distance < min_distance:
            min_distance = distance
            best_path = path
    return best_path, min_distance

def measure_time(func: Callable[..., Any], *args: object) -> tuple[Any, float]:
    """Measure the execution time of a function."""
    start = time.perf_counter()
    result = func(*args)
    duration = time.perf_counter() - start
    return result, duration

def run(config: dict) -> None:
    """Run the SAT and TSP algorithms."""
    logger.info("Vérification SAT :")
    sat_data = config.get("sat", {})
    clauses = sat_data.get("clauses", [])
    assignment = sat_data.get("assignment", {})
    if clauses and assignment:
        (result, t_sat) = measure_time(is_satisfiable, clauses, assignment)
        logger.info(f"Résultat : {'Satisfiable' if result else 'Non satisfiable'}")
        logger.info(f"Temps SAT : {t_sat:.6f} s")
    else:
        logger.error("Pas de données SAT fournies.")

    logger.info("Heuristique TSP (plus proche voisin) :")
    tsp_data = config.get("tsp", {})
    matrix = tsp_data.get("distances", [])
    matrix_length_limit = 8
    if matrix:
        (approx_result, t_heuristic) = measure_time(tsp_nearest_neighbor, matrix)
        logger.info(f"Chemin heuristique : {approx_result[0]}")
        logger.info(f"Distance heuristique : {approx_result[1]}")
        logger.info(f"Temps heuristique : {t_heuristic:.6f} s")

        if len(matrix) <= matrix_length_limit:
            (brute_result, t_brute) = measure_time(tsp_brute_force, matrix)
            logger.info(f"Chemin optimal (brute force) : {brute_result[0]}")
            logger.info(f"Distance brute force : {brute_result[1]}")
            logger.info(f"Temps brute force : {t_brute:.6f} s")
        else:
            logger.error("Graphe trop grand pour brute force (>8 noeuds).")
    else:
        logger.error("Pas de données TSP fournies.")
