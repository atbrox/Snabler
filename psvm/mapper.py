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

def run_mapper(map, separator="\t"):
    data = read_input(sys.stdin,separator)
    for (key,value) in data:
        map(key,value)

def map(key, value):
    trainingclasses = [float(i) for i in key.split(",")]
    trainingfeatures = [float(i) for i in value.split(",")]

    # if more than one class in classes, the features contains
    # |classes| consecutive training example feature vectors
    # so need to reshape it, to have 1 per row
    numtrainingclasses = len(trainingclasses)
    numtrainingfeatures = len(trainingfeatures)
    numfeaturesperexample = numtrainingfeatures/numtrainingclasses

    A = numpy.matrix(
        numpy.reshape(numpy.array(trainingfeatures), 
                      (numtrainingclasses,numfeaturesperexample)))
    D = numpy.diag(trainingclasses)
    e = numpy.matrix(numpy.ones(len(A)).reshape(len(A),1))
    E = numpy.matrix(numpy.append(A,-e,axis=1))

    value = base64.b64encode(pickle.dumps((E.T*E, E.T*D*e)))
    print "outputkey\t%s" % ( value )

if __name__ == "__main__":
    run_mapper(map)
