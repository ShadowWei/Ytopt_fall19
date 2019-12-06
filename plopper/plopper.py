import os
import sys
import subprocess
import random
import config as cfg
import cProfile

class Plopper:

    needLine = "nothing is passing"
    def __init__(self):
        # Initilizing global variables
        self.configfile = os.path.dirname(os.path.abspath(__file__))+'/config.txt'
        self.sourcefile = cfg.sourcefile
        self.outputdir = cfg.outputdir+"/tmp_files"
        self.compileoptions = cfg.compileoptions
        self.sourcedir = cfg.sourcedir

        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
         

    #Creating a dictionary using parameter label and value 
    def createDict(self, x, params):
        dictVal = {}
        for p, v in zip(params, x):
            dictVal[p] = v
        return(dictVal)

    #Replace the Markers in the source file with the corresponding Pragma values
    def plotValues(self, dictVal, inputfile, outputfile):
        with open(inputfile, "r") as f1:
            buf = f1.readlines()
                
        with open(outputfile, "w") as f2:
            for line in buf:
                modify_line = line
                for key, value in dictVal.items():
                    if key in modify_line:
                        if value != 'None': #For empty string options
                            modify_line = modify_line.replace('#'+key, str(value))
                            #print(modify_line)

                        else:
                            modify_line = modify_line.replace('#'+key, "")
                
                if modify_line != line:
                    needLine = modify_line
                    print("this is modline" + needLine)
                    f2.write(modify_line)
                else:
                    #To avoid writing the Marker
                    f2.write(line)

    def dummy(self, cmd):
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    # Function to find the execution time of the interim file, and return the execution time as cost to the search module
    def findRuntime(self, x, params, valid):
        interimfile = ""
        #exetime = float('inf')
        exetime = sys.maxsize
        counter = random.randint(1, 10001) # To reduce collision increasing the sampling intervals

        interimfile = self.outputdir+"/"+str(counter)+".c"

        # Generate intermediate file
        dictVal = self.createDict(x, params)
        self.plotValues(dictVal, self.sourcefile, interimfile)

        #compile and find the execution time
        tmpbinary = interimfile[:-2]

        #cmd1 = "gcc -fopenmp -DPOLYBENCH_TIME -DLARGE_DATASET -O2 -I"+self.sourcedir+"/utilities -I"+self.sourcedir+"/atax "+interimfile + " -o "+tmpbinary+" -lm"

        if(valid):
            cmd1 = "gcc -fopenmp -DPOLYBENCH_TIME -DEXTRALARGE_DATASET -O2 -I"+self.sourcedir+"/utilities -I"+self.sourcedir+"/convolution-2d "+interimfile+" "+self.sourcedir+"/utilities/polybench.c -o "+tmpbinary+" -lm"

            print("cmd1" + cmd1)

            cmd2 = tmpbinary+" "+self.compileoptions
            
            print("cmd2" + cmd2) #printing cmd2 

        #Find the compilation status using subprocess
        #compilation_status = subprocess.run(cmd1, shell=True, stderr=subprocess.PIPE)
        
    
            file_name = tmpbinary + ".log"
            file_err = open(file_name, 'w')
    
            compilation_status = subprocess.run(cmd1, shell=True, stderr=file_err)
            file_err.close()

        #Find the execution time only when the compilation return code is zero, else return infinity
        #if compilation_status.returncode != 0:#check
        #    print("Compilation stat: not equal 0" + cmd2)

        #if len(compilation_status.stderr) != 0: #check
        #print("len comp stat: !=0" + cmd2)

            if compilation_status.returncode == 0: #Second condition is to check for warnings
                execution_status = subprocess.run(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                exetime = float(execution_status.stdout.decode('utf-8').split('\n')[0])
                print(exetime)
        
        return exetime #return execution time as cost


if __name__ == '__main__':
    params = ["P1", "P2", "P3"]
    x = ["static", "8", "2"]
    obj = Plopper()
    retVal = obj.findRuntime(x, params)
    print(retVal)
