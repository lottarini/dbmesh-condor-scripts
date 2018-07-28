import os
import re
import sys
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler'))
from scheduling_analyzer_single import analyze_stats

#library = "synopsys"
library = "tsmc"
if library == "synopsys":
    dbmesh_core_area = 26835.57356 + 11380.5686 # core + switch router
    freq = 200 # freq in MHz of the dbmesh core
elif library == "tsmc":
    dbmesh_core_area = 36897.120848 + 12111.1203
    freq = 900
else:
    raise NotImplementedError

working_queries = [1,2,3,4,5,6,7,8,9,10,11,12,14,16,17,18,19,20,22]

def get_latencies(d):
    latency = []
    for i in range(1,23):
        stat_file = os.path.join(d,str(i),"stats")
        if os.path.isfile(stat_file):
            with open(stat_file) as f:
                icc,cc,_,_,_ = analyze_stats(f)
                    
                latency.append( cc ) 
                #print "{:<4}\t{:>10}".format(i,cc)
        else:
            latency.append(0)
            
    return latency

if __name__ == "__main__":
    
    for d in os.listdir("."):
        m = re.match("DSE_([0-9]+)_([0-9]+)",d)
        if m:
            #print m.groups()
            width = int(m.groups()[0])
            depth = int(m.groups()[1])
            area  = width * depth * dbmesh_core_area
            latencies = get_latencies(d)
            if latencies is not None:
                latency = sum(latencies) * float( 1.0 / float(freq * 1000) ) # normalize to ms instead of sec
                print width, depth, area, latency
