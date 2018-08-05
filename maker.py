import os
import sys
import errno
import shutil
'''
This script will create a set of dirs 1-22 in folder sys.arg[1] and create appropriate scripts for condor execution
'''


try:
    assert os.path.isdir(sys.argv[1]) #directory where all folders are created
    width = int(sys.argv[2])
    depth = int(sys.argv[3])
    schedule = sys.argv[4]
    assert schedule in ["real","ideal","dumb"]
except:
    print >> sys.stderr , "Usage: maker.py <folder> <width> <depth> <schedule_algo>"
    raise


#condor_scripts = [ "script", "condor.submit"]
condor_scripts = [ "condor.submit","cut.py"]

for e in condor_scripts:
    assert os.path.isfile(e)
    # copy the condor scripts
    #os.symlink(os.path.abspath(e), os.path.abspath(os.path.join(sys.argv[1],e)))
    shutil.copy(os.path.abspath(e), os.path.abspath(os.path.join(sys.argv[1],e)))
    
assert os.path.isfile("script")
dest = os.path.join(sys.argv[1],"script")
assert os.path.abspath("script") != os.path.abspath(dest)
with open("script") as f , open(dest,'w') as g:
    for line in f:

        line = line.replace("$2",str(width))
        line = line.replace("$3",str(depth))
        line = line.replace("$4",schedule)

        g.write(line)
os.chmod(dest,0744)

for i in xrange(1,23):
    new_dir = os.path.join(sys.argv[1],str(i))

    try:
        os.makedirs( new_dir )
    except OSError as exception: #it is fine if the directory is already there
        if exception.errno != errno.EEXIST:
            raise    
