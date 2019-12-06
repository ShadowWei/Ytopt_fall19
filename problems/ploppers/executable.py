#!/usr/bin/env python
from __future__ import print_function
import re
import os
import sys
import time
import json
import math
import os
import argparse
import numpy as np

sys.path.insert(0, '/uufs/chpc.utah.edu/common/home/u1074259/ytopt/plopper')
from plopper import Plopper

from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
seed = 12345

def create_parser():
    'command line parser'
    
    parser = argparse.ArgumentParser(add_help=True)
    group = parser.add_argument_group('required arguments')

    for id in range(0, 7):
        parser.add_argument('--p%d'%id, action='store', dest='p%d'%id,
                            nargs='?', const=6, type=str, default='a',
                            help='parameter p%d value'%id)
    return(parser)

parser = create_parser()
cmdline_args = parser.parse_args()
param_dict = vars(cmdline_args)

p0 = param_dict['p0']
p1 = param_dict['p1']
p2 = param_dict['p2']
p3 = param_dict['p3']
p4 = param_dict['p4']
p5 = param_dict['p5']
p6 = param_dict['p6']

x=[p0,p1,p2,p3,p4,p5,p6]

p0_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp parallel for schedule(#p3, #p4) collapse(#p6) num_threads(#p5)", 'd': "#pragma omp target teams distribute"}
p1_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp parallel for schedule(#p3, #p4) collapse(#p6) num_threads(#p5)"}
p2_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp simd"}
p3_dict = {'a': "static", 'b': "dynamic"}
p4_dict = {'a': "1", 'b': "8", 'c': "16"}
p5_dict = {'a': "1", 'b': "2", 'c': "4", 'd': "8", 'e': "14", 'f': "16", 'g': "28"}
p6_dict = {'a': "1", 'b': "2"}

obj = Plopper()
def plopper_func(x):
    value = [p0_dict[x[0]], p1_dict[x[1]], p2_dict[x[2]], p3_dict[x[3]], p4_dict[x[4]], p5_dict[x[5]], p6_dict[x[6]]]
    params = ["LOOP1", "LOOP2", "LOOP3", "p3", "p4", "p5", "p6"]

    result = obj.findRuntime(value, params)

    return result

pval = plopper_func(x)
print('OUTPUT:%1.3f'%pval)
