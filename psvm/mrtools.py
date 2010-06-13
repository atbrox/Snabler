# #!/usr/bin/env python
# encoding: utf-8

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

def run_reducer(reduce,separator="\t"):
    data = read_input(sys.stdin,
                      separator)
    for key, values in groupby(data, itemgetter(0)):
        reduce(key, values)

