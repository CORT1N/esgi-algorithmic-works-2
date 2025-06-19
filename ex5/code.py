"""Fifth exercise."""
import random
import time

from logger import logger


def quicksort_random(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quicksort_random(less) + equal + quicksort_random(greater)


def quicksort_deterministic(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]  # déterministe
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    return quicksort_deterministic(less) + [pivot] + quicksort_deterministic(greater)

def measure_time(func, arr):
    start = time.perf_counter()
    result = func(arr[:])  # copie pour ne pas modifier l'original
    end = time.perf_counter()
    return result, end - start

def run(config):
    test_arrays = config.get("test_arrays", [])
    if not test_arrays:
        logger.error("Aucun tableau de test fourni dans la config.")
        return

    for i, arr in enumerate(test_arrays, 1):
        logger.info(f"Test {i} avec le tableau : {arr}")

        res_det, time_det = measure_time(quicksort_deterministic, arr)
        logger.info(f"Tri rapide déterministe : résultat = {res_det}, temps = {time_det:.6f}s")

        res_rand, time_rand = measure_time(quicksort_random, arr)
        logger.info(f"Tri rapide randomisé : résultat = {res_rand}, temps = {time_rand:.6f}s")