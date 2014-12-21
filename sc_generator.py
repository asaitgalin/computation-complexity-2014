# -*- coding: utf-8 -*-

import random

def generate_random_sc_problem(n):
    X = list(range(1, n + 1))
    k = random.randint(1, n)
    F = list()
    while k > 0:
        length = random.randint(1, len(X))
        subset = set(random.sample(X, length))
        F.append(subset)
        k -= 1
    uncovered = set(X)
    for f in F:
        uncovered -= f
    if len(uncovered) > 0:
        F.append(uncovered)
    return set(X), F

