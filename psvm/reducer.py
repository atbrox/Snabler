#!/usr/bin/env python
# encoding: utf-8

import base64
import cPickle as pickle
import logging
import numpy

#import mrtools

from itertools import groupby
from operator import itemgetter
import sys

def read_input(file, separator="\t"):
    for line in file:
        yield line.rstrip().split(separator)

def run_reducer(reduce,separator="\t"):
    data = read_input(sys.stdin,
                      separator)
    for key, values in groupby(data, itemgetter(0)):
        reduce(key, values)


def reduce(key, values, mu=0.1):
    sumETE = None
    sumETDe = None
    
    for _, value in values:
        ETE, ETDe = pickle.loads(base64.b64decode(value))
        if sumETE == None:
            sumETE = numpy.matrix(numpy.eye(ETE.shape[1])/mu)
        sumETE += ETE
            
        if sumETDe == None:
            sumETDe = ETDe
        else:
            sumETDe += ETDe

    result = sumETE.I*sumETDe
    print "%s\t%s" % (key, str(result.tolist()))

if __name__ == "__main__":
    run_reducer(reduce)
