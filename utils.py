# -*- coding: utf8 -*-

import time

def timeit(f):
    def wrap(*args, **kwargs):
        startTime = time.clock()
        value = f(*args, **kwargs)
        print('Function {0} execution time: {1:.5f}s'.format(f.__name__, time.clock() - startTime))
        return value
    return wrap

