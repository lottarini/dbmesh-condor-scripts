import os
import sys
import errno

'''
This script will create a set of dirs 1-sys.arg[1]
and a condor script to launch a q100 DSE
'''

condor_base = "executable = ./script \n \
universe = vanilla \n \
output = main.out \n \
error = main.err \n \
log = main.log \n \
getenv = True \n"

with open("condor.submit",'w') as f:
    f.write(condor_base)
    for i in range(int(sys.argv[1])):
        f.write("initial_dir = {} \narguments = {} \nqueue\n".format(i,i))
        try:
            os.makedirs( str(i) )
        except OSError as exception: #it is fine if the directory is already there
            if exception.errno != errno.EEXIST:
                raise    
        
