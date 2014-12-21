#!/usr/bin/env python

import sys, os
import msc_benchmark_reader
import or_benchmark_reader
from utils import timeit
import sc_greedy
from collections import defaultdict
from pulp import *
import matplotlib.pyplot as plt
import numpy as np
import sc_generator

# DATASET: ("folder", "data extension", "data reader class")
DATASETS = [("dataset1", ".msc", msc_benchmark_reader.BenchmarkDataReader),
            ("dataset2", ".txt", or_benchmark_reader.BenchmarkDataReader)]

DEBUG = False

@timeit
def find_coverage_greedy(X, F):
    return sc_greedy.find_coverage(X, F)

def read_optimal_cover_size(f):
    filename = os.path.join(f + '.opt')
    try:
        with open(filename, 'r') as f:
            return int(f.readline())
    except IOError:
        return None

def run_greedy_algorithm(X, F, optimal_size):
    print("Starting greedy algorithm")
    S = find_coverage_greedy(X, F)
    if optimal_size is None:
        print("Found coverage size: {}".format(len(S)))
    else:
        print("Found coverage size: {}, optimal: {}".format(len(S), optimal_size))
    return len(S)

def get_max_element_frequency(X, F):
    max_freq = None
    for x in X:
        freq = 0
        for f in F:
            if x in f:
                freq += 1
        max_freq = freq if (max_freq is None or freq > max_freq) else max_freq
    return max_freq

@timeit
def find_coverage_simplex(X, F, freq):
    variables = [LpVariable("x{}".format(i), 0, 1) for i in range(1, len(F) + 1)]
    p = LpProblem(sense = LpMinimize)
    p += sum(variables)

    for x in X:
        s = None
        for subset_index, subset in enumerate(F):
            if x in subset:
                if s is None:
                    s = variables[subset_index]
                else:
                    s += variables[subset_index]
        p += s >= 1

    status = p.solve(GLPK(msg=0))
    if DEBUG:
        print([value(v) for v in variables])
    subsets = map(
        lambda x: 1 if x >= 1.0 / freq else 0,
        [value(v) for v in variables]
    )
    return sum(subsets)

def run_simplex_algorithm(X, F, optimal_size):
    freq = get_max_element_frequency(X, F)
    print("Starting simplex algorithm with k = {}".format(freq))
    S = find_coverage_simplex(X, F, freq)
    if optimal_size is None:
        print("Found coverage size: {}".format(S))
    else:
        print("Found coverage size: {}, optimal: {}".format(S, optimal_size))

def process_file(f, rel_path, reader_cls):
    filename = os.path.join(rel_path, f)
    X, F = reader_cls.read_file(filename)
    print("Read data from {}, X size: {}, F size: {}".format(f, len(X), len(F)))
    optimal_size = read_optimal_cover_size(filename)
    run_greedy_algorithm(X, F, optimal_size)
    run_simplex_algorithm(X, F, optimal_size)

def run_greedy_counterexamples_demo():
    xlist = list()
    ylist = list()

    for k in range(3, 10):
        X, F, optimal_size = generate_bad_example_for_greedy_algorithm(k)
        print("Autogenerated bad example for greedy algorithm with k = {}, X size: {}, F size: {}".format(
            k, len(X), len(F)
        ))
        xlist.append(len(X))
        out_size = run_greedy_algorithm(X, F, optimal_size)
        run_simplex_algorithm(X, F, optimal_size)
        ylist.append(out_size)

    # Plot results
    x = np.array(xlist)
    y = np.array(ylist)
    print("Plotting results (curve should look like log2(n))")
    plt.plot(x, y, label="greedy")
    plt.plot(x, np.log2(x), label="log2")
    plt.plot(x, np.repeat([2], len(y)), label="optimal")
    plt.xlim(1, 1000)
    plt.ylim(0, 15)
    plt.xlabel("size of universe (X)")
    plt.ylabel("set cover size (greedy algorithm)")
    plt.legend()
    plt.show()

def plot_random_dataset_comparison():
    # It is platform dependent so it is hardcoded
    k = np.array([21, 38, 45, 53])
    greedy_results = np.array([1.12, 1.34, 1.47, 2.34])
    linear_results = np.array([57.68, 122.36, 220.57, 288.29])
    fig, ax = plt.subplots()
    indices = np.arange(1, 5)
    width = 0.35
    ax.bar(indices, np.log(greedy_results), width, color='r', label='greedy')
    ax.bar(indices + width, np.log(linear_results), width, color='b', label='linear_prog')
    ax.set_xlabel('k (each element of X occurs in <= k subsets)')
    ax.set_ylabel('ln(time)')
    ax.set_xticks(indices + width)
    ax.set_xticklabels(k)
    ax.legend()
    plt.show()

def run_datasets_demo():
    for ds in DATASETS:
        print("Getting data from \"{}\" directory".format(ds[0]))
        for f in os.listdir(ds[0]):
            p, ext = os.path.splitext(f)
            if ext == ds[1]:
                process_file(f, ds[0], ds[2])

def run_random_demo():
    for i in range(20, 100):
        X, F = sc_generator.generate_random_sc_problem(i)
        print("Autogenerated random set cover problem, X size: {}, F size: {}".format(
            len(X), len(F)
        ))
        run_greedy_algorithm(X, F, None)
        run_simplex_algorithm(X, F, None)

def main():
    print("Starting set cover problem algorithms demo")
    run_datasets_demo()
    run_greedy_counterexamples_demo()
    run_random_demo()
    plot_random_dataset_comparison()

if __name__ == '__main__':
    main()

