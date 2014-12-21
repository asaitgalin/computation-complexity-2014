#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

''' This file provides BenchmarkDataReader class for set cover problem benchmark (msc format)
    Input benchmark file format:

    First line has form "p set U S", where U, S - natural numbers
    (number of elements in the universe and number of subsets in the collection)

    The remaining of the file is a list of lines starting with "s" which indicate the subsets in the collection
    (e.g. the line "s 1 2 4" indicates that there is a subset with three elements which are 1, 2 and 4).
'''

__all__  = ['BenchmarkDataReader']

class BenchmarkDataReader(object):

    ''' Returns tuple with (X, F)
        Argument: filename - file to be processed
    '''
    @classmethod
    def read_file(cls, filename):
        X = None
        F = list()
        with open(filename, mode = 'r') as f:
            xsize, fsize = cls.__read_header(f)
            for line in f:
                subset = [int(x) for x in line.split()[1:]]
                F.append(set(subset))
            X = set(range(1, xsize + 1))
        return X, F

    @staticmethod
    def __read_header(f):
        try:
            xsize, fsize = [int(x) for x in f.readline().split()[2:]]
        except ValueError:
            sys.stderr.write("Error in file {}: Incorrect input file format (no header)".format(f.name)
                + os.linesep)
            sys.exit(1)
        return xsize, fsize


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: {} benchmark_data_file_name".format(
            os.path.basename(sys.argv[0])
        ) + os.linesep)
        sys.exit(1)

    X, F = BenchmarkDataReader.read_file(sys.argv[1])
    print(X, F)

if __name__ == '__main__':
    main()

