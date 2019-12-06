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

    for id in range(0, 27):
        parser.add_argument('--p%d'%id, action='store', dest='p%d'%id,
                            nargs='?', const=26, type=str, default='a',
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
p5 = param_dict['p5'] #DS_dict  
p6 = param_dict['p6'] #SC_dict
p7 = param_dict['p7'] #NT_dict
p8 = param_dict['p8'] #CO_dict
p9 = param_dict['p9'] #TL_dict
p10 = param_dict['p10'] #static or dynamic  
p11 = param_dict['p11'] #1, 8, 16  Chunk Size? 
p12 = param_dict['p12'] #1, 2, 4, 8, 14, 16, 28 NT
p13 = param_dict['p13'] #1, 2, 3    Collapse
p14 = param_dict['p14'] #32, 64, 128, 256   thread limit
p15 = param_dict['p15'] #PF2_dict
p16 = param_dict['p16'] #SI2_dict p4
p17 = param_dict['p17'] #DS2_dict p5 
p18 = param_dict['p18'] #SC2_dict p6
p19 = param_dict['p19'] #NT2_dict p7
p20 = param_dict['p20'] #CO2_dict p8
p21 = param_dict['p21'] #TL2_dict p9
p22 = param_dict['p22'] #static or dynamic
p23 = param_dict['p23'] #1, 8, 16  Chunk Size
p24 = param_dict['p24'] #1, 2, 4, 8, 14, 16, 28 NT
p25 = param_dict['p25'] #1, 2, 3    Collapse
p26 = param_dict['p26'] #32, 64, 128, 256   thread limit

x=[p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26]  

#first loop
p0_dict = {'a': "None", 'b': "#pragma omp #p3 private(j)", 'c': "#pragma omp target teams distribute #p3 #p5 private(j)", 'd': "#pragma omp #p4"} #p0     #loop1?
p1_dict = {'a': "None", 'b': "#pragma omp #p15", 'c': "#pragma omp target teams distribute #p15 #p17", "d": "#pragma omp #p16"} #p1  #loop2?
p2_dict = {'a': "None", 'b': "#pragma omp #p3", 'c': "#pragma omp target teams distribute #p4 #p5"} #p2     #need? #not currently used
PF_dict = {'a': "None", 'b': "parallel for #p4 #p6 #p7"} #p3
SI_dict = {'a': "None", 'b': "simd"} #p4
DS_dict = {'a': "None", 'b': "dist_schedule(static, #p11)"}#p5 #p11 chunk size 
SC_dict = {'a': "None", 'b': "schedule(#p10, #p12)", 'c': "schedule(#p10)"} #p6 static or dynamic numthreads
NT_dict = {'a': "None", 'b': "num_threads(#p12)"} #p7
CO_dict = {'a': "None", 'b': "collapse(#p13)"} #p8
TL_dict = {'a': "None", 'b': "thread_limit(#p14)"} #p9
#second loop
PF2_dict = {'a': "None", 'b': "parallel for #p16 #p18 #p19"} #p15
SI2_dict = {'a': "None", 'b': "simd"} #p16 need simd 
DS2_dict = {'a': "None", 'b': "dist_schedule(static, #p23)"}
SC2_dict = {'a': "None", 'b': "schedule(#p22, #p24)", 'c': "schedule(#p22)"} #p17
NT2_dict = {'a': "None", 'b': "num_threads(#p24)"} #p18
CO2_dict = {'a': "None", 'b': "collapse(#p25)"} #p19
TL2_dict = {'a': "None", 'b': "thread_limit(#p26)"} #p20 

obj = Plopper()
def plopper_func(x):
    
    valid = True    
    
    #invalid problem set conditions: 
    if x[0] == 'b' and x[3] == 'a':#
        valid = False
    if x[1] == 'b' and x[15] == 'a':#
        valid = False
    if x[1] == 'b' and x[4] == 'b':#
        valid = False
    if x[0] == 'd' and x[4] == 'a':#p0_dict is d and SI_dict is not none 
        valid = False
    if x[1] == 'd' and x[16] == 'a':#p1_dict is d and SI2_dict is not none
        valid = False
    
    
    print("valid next line:")
    print(bool(valid))

    value = [p0_dict[x[0]], p1_dict[x[1]], p2_dict[x[2]], PF_dict[x[3]], SI_dict[x[4]], DS_dict[x[5]], SC_dict[x[6]], NT_dict[x[7]], CO_dict[x[8]], TL_dict[x[9]], p10, p11, p12, p13, p14, PF2_dict[x[15]], SI2_dict[x[16]], DS2_dict[x[17]], SC2_dict[x[18]], NT2_dict[x[19]], CO2_dict[x[20]], TL2_dict[x[21]], p22, p23, p24, p25, p26]

    
    params = ["LOOP1", "LOOP2", "LOOP3", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p25", "p26"]


    result = obj.findRuntime(value, params, valid)

    return result

pval = plopper_func(x)
print('OUTPUT:%1.3f'%pval)
