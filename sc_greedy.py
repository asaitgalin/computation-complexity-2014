# -*- coding: utf-8 -*-

from copy import deepcopy

# Simple implementation of greedy algorithm (finds set coverage)
def find_coverage(X, F):
    max_cover_set_index = None
    coverage_indices = list()
    while True:
        uncovered = deepcopy(X)
        for i in coverage_indices:
            uncovered -= F[i]
        if len(uncovered) < 1:
            break
        available_sets = [(n, f) for (n, f) in enumerate(F) if n not in coverage_indices]
        if not available_sets:
            raise RuntimeError("not enough sets in F")
        for n, f in available_sets:
            if max_cover_set_index is None:
                max_cover_set_index = n
            else:
                a = uncovered - f
                b = uncovered - F[max_cover_set_index]
                if len(uncovered - f) < len(uncovered - F[max_cover_set_index]):
                    max_cover_set_index = n
        coverage_indices.append(max_cover_set_index)
        max_cover_set_index = None

    return [f for (n, f) in enumerate(F) if n in coverage_indices]

def generate_bad_example_for_greedy_algorithm(k):
    optimal = 2
    X_size = 2 ** (k + 1) - 2
    X = set(range(1, X_size + 1))
    F = list()
    F.append(set( range(1, X_size / 2 + 1) ))
    F.append(set( range(X_size / 2 + 1, X_size + 1) ))
    cursor = 1
    for i in range(k):
        F.append(set())
        for j in range(2 ** i):
            F[-1].add(cursor)
            F[-1].add(X_size / 2 + cursor)
            cursor += 1
    return X, F, optimal
