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

    for id in range(0, 14):
        parser.add_argument('--p%d'%id, action='store', dest='p%d'%id,
                            nargs='?', const=13, type=str, default='a',
                            help='parameter p%d value'%id)
    return(parser)

parser = create_parser()
cmdline_args = parser.parse_args()
param_dict = vars(cmdline_args)

p0 = param_dict['p0'] #p0_dict
p1 = param_dict['p1'] #p1_dict
p2 = param_dict['p2'] #p2_dict
p3 = param_dict['p3'] #PF_dict
p4 = param_dict['p4'] #SI_dict
p5 = param_dict['p5'] #SC_dict
p6 = param_dict['p6'] #NT_dict
p7 = param_dict['p7'] #CO_dict
p8 = param_dict['p8'] #TL_dict
p9 = param_dict['p9'] #static or dynamic  
p10 = param_dict['p10'] #1, 8, 16  Chunk Size? 
p11 = param_dict['p11'] #1, 2, 4, 8, 14, 16, 28 NT? 
p12 = param_dict['p12'] #1, 2, 3    Collapse
p13 = param_dict['p13'] #32, 64, 128, 256   thread limit?

p14 = param_dict['p4'] #SI_dict                                       
p15 = param_dict['p5'] #SC_dict                                       
p16 = param_dict['p6'] #NT_dict                                       
p17 = param_dict['p7'] #CO_dict                                       
p18 = param_dict['p8'] #TL_dict                                       
p19 = param_dict['p9'] #static or dynamic                             
p20 = param_dict['p10'] #1, 8, 16  Chunk Size?                       
p21 = param_dict['p11'] #1, 2, 4, 8, 14, 16, 28 NT?                  
p22 = param_dict['p12'] #1, 2, 3    Collapse                         
p23 = param_dict['p13'] #32, 64, 128, 256   thread limit?  

x=[p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13]
print(x)

p0_dict = {'a': "None", 'b': "#pragma omp #p3", 'c': "#pragma omp target teams distribute #p4 #p8"} #p0
p1_dict = {'a': "None", 'b': "#pragma omp #p3", 'c': "#pragma omp target teams distribute #p4 #p8"} #p1
p2_dict = {'a': "None", 'b': "#pragma omp #p3", 'c': "#pragma omp target teams distribute #p4 #p8"} #p2
PF_dict = {'a': "None", 'b': "parallel for #p4 #p5 #p6"} #p3
SI_dict = {'a': "None", 'b': "simd"} #p4
SC_dict = {'a': "None", 'b': "schedule(#p9, #p11)"} #p5
NT_dict = {'a': "None", 'b': "num_threads(#p11)"} #p6
CO_dict = {'a': "None", 'b': "collapse(#p12)"} #p7
TL_dict = {'a': "None", 'b': "thread_limit(#p13)"} #p8
#SI_dict = {'a': "None", 'b': "simd"} #p

#p0_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp parallel for schedule(#p3, #p4) collapse(#p6) num_threads(#p5)", 'd': "#pragma omp target teams distribute"}
#p1_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp parallel for schedule(#p3, #p4) collapse(#p6) num_threads(#p5)"}
#p2_dict = {'a': "None", 'b': "#pragma omp parallel for schedule(#p3, #p4) num_threads(#p5)", 'c': "#pragma omp simd"}
#p3_dict = {'a': "static", 'b': "dynamic"}
#p4_dict = {'a': "1", 'b': "8", 'c': "16"}
#p5_dict = {'a': "1", 'b': "2", 'c': "4", 'd': "8", 'e': "14", 'f': "16", 'g': "28"}
#p6_dict = {'a': "1", 'b': "2", 'c': "3"}

obj = Plopper()
def plopper_func(x):
    #value = [p0_dict[x[0]], p1_dict[x[1]], p2_dict[x[2]], p3, p4, p5, p6, p7, PF_dict[x[8]], SI_dict[x[9]], SC_dict[x[10]], NT_dict[x[11]], CO_dict[x[12]], TL_dict[x[13]]]   
    print("hello")
    value = [p0_dict[x[0]], p1_dict[x[1]], p2_dict[x[2]], PF_dict[x[3]], SI_dict[x[4]], SC_dict[x[5]], NT_dict[x[6]], CO_dict[x[7]], TL_dict[x[8]], p9, p10, p11, p12, p13]
    print("BYE")
    
    params = ["LOOP1", "LOOP2", "LOOP3", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13"]
    

    result = obj.findRuntime(value, params)

    return result

pval = plopper_func(x)
print('OUTPUT:%1.3f'%pval)
