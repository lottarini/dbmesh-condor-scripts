import os
import re
import sys
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler'))
from scheduling_analyzer_single import analyze_stats
from martha_plot import succesful

working_queries = [1,2,3,4,5,6,7,8,9,10,11,12,14,16,17,18,19,20,22]

def last_line(out_file):
    line = ""
    with open(out_file) as f:
        for line in f:
            pass
        
    return line

if __name__ == "__main__":
    
    for d in os.listdir("."):
        m = re.match("DSE_",d)
        if m:
            for i in working_queries:

                out_file  = os.path.join(d,str(i),"main.out")
                if not os.path.isfile(out_file):
                    print out_file, "MISSING"
                elif not succesful(out_file):
                    print out_file, "\n",last_line(out_file)
