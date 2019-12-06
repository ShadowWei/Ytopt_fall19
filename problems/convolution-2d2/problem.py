from collections import OrderedDict
import numpy as np
import os 

np.random.seed(0)

HERE = os.path.dirname(os.path.abspath(__file__))

from ytopt.problem import Problem

cmd_frmt = "python " +HERE+"/executable.py"
nparam = 27

for i in range(0, nparam):
    cmd_frmt += f" --p{i} {'{}'}"
problem = Problem(cmd_frmt)

problem.spec_dim(p_id=0, p_space=['a', 'b', 'c', 'd'], default='b') #p0_dict
problem.spec_dim(p_id=1, p_space=['a', 'b', 'c', 'd'], default='b') #p1_dict
problem.spec_dim(p_id=2, p_space=['a', 'b', 'c'], default='c') #p2_dict
problem.spec_dim(p_id=3, p_space=['a', 'b'], default='b') #PF_dict
problem.spec_dim(p_id=4, p_space=['a', 'b'], default='b') #SI_dict
problem.spec_dim(p_id=5, p_space=['a', 'b'], default='b') #DS_dict
problem.spec_dim(p_id=6, p_space=['a', 'b', 'c'], default='c') #SC_dict
problem.spec_dim(p_id=7, p_space=['a', 'b'], default='b') #NT_dict
problem.spec_dim(p_id=8, p_space=['a', 'b'], default='b') #CO_dict
problem.spec_dim(p_id=9, p_space=['a', 'b'], default='b') #TL_dict
problem.spec_dim(p_id=10, p_space=['static', 'dynamic'], default='static') #stat or dyn
problem.spec_dim(p_id=11, p_space=['1', '8', '16'], default='8') #chunk size
problem.spec_dim(p_id=12, p_space=['2', '4', '8', '14', '16', '28'], default='4') #NT param
problem.spec_dim(p_id=13, p_space=['1', '2', '3'], default='1') #collapse param
problem.spec_dim(p_id=14, p_space=['32', '64', '128', '256'], default ='128') # tl param
problem.spec_dim(p_id=15, p_space=['a', 'b'], default='b') #PF2_dict  
problem.spec_dim(p_id=16, p_space=['a', 'b'], default='b') #SI2_dict
problem.spec_dim(p_id=17, p_space=['a', 'b'], default='b') #DS2dict
problem.spec_dim(p_id=18, p_space=['a', 'b', 'c'], default='c') #SC2_dict
problem.spec_dim(p_id=19, p_space=['a', 'b'], default='b') #NT2_dict
problem.spec_dim(p_id=20, p_space=['a', 'b'], default='b') #CO2_dict
problem.spec_dim(p_id=21, p_space=['a', 'b'], default='b') #TL2_dict 
problem.spec_dim(p_id=22, p_space=['static', 'dynamic'], default='static') #stat or dyn
problem.spec_dim(p_id=23, p_space=['1', '8', '16'], default='8') #chunk size
problem.spec_dim(p_id=24, p_space=['2', '4', '8', '14', '16', '28'], default='4') #NT param
problem.spec_dim(p_id=25, p_space=['1', '2', '3'], default='1') #collapse param
problem.spec_dim(p_id=26, p_space=['32', '64', '128', '256'], default ='128') # tl param

problem.checkcfg()

if __name__ == '__main__':
    print(problem)
