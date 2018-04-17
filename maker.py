import os
import sys
import errno

assert os.path.isdir(sys.argv[1]) #directory where all folders are created

'''
This script will create a set of dirs 1-22 in folder sys.arg[1] 
'''

for i in xrange(1,23):
    new_dir = os.path.join(sys.argv[1],str(i))

    try:
        os.makedirs( new_dir )
    except OSError as exception: #it is fine if the directory is already there
        if exception.errno != errno.EEXIST:
            raise
