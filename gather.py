import os
import re
import sys
import pdb
# sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler'))
# from scheduling_analyzer_single import analyze_stats

#library = "synopsys"
library = "tsmc"
if library == "synopsys":
    dbmesh_core_area = 26835.57356 + 11380.5686 # core + switch router
    freq = 200 # freq in MHz of the dbmesh core
    raise NotImplementedError
elif library == "tsmc":
    dbmesh_core_area = 36897.120848 + 12111.1203
    freq = 900
    router_static_pwr  = 0.000125
    router_dynamic_pwr = 0.000308
    dbmesh_static_pwr  = 0.000611
    dbmesh_dynamic_pwr = 0.009015
else:
    raise NotImplementedError

working_queries = [1,2,3,4,5,6,7,8,9,10,11,12,14,16,17,18,19,20,22]

def get_latencies(d):
    latency = []
    noc_cycles = []
    compute_cycles = []
    for i in range(1,23):
        stat_file = os.path.join(d,str(i),"stats")
        if os.path.isfile(stat_file):
            with open(stat_file) as f:
                cc,tcc,ncc = analyze_stats(f)
                    
                latency.append( cc )
                noc_cycles.append(ncc)
                compute_cycles.append(tcc)
                #print "{:<4}\t{:>10}".format(i,cc)
        else:
            latency.append(0)
            
    return latency, compute_cycles, noc_cycles

def analyze_stats(stat_file):

    query_latency = 0

    tile_utilization = 0
    noc_utilization = 0
    for stat_line in stat_file:
        if re.search("Area",stat_line):
            continue
        values = stat_line.split(",")
        assert len(values) > 1, "Something wrong with this line: {} in this file: {}".format(stat_line,stat_file)
        if (values[1] == "DIRECTIVE"):
            directive_latency = float(values[2])
            query_latency += directive_latency
            assert  values[2] == values[3] 

            try:
                tile_utilization +=  int(values[6])  * directive_latency
                noc_utilization  +=  ( int(values[7]) + int(values[6]) )  * directive_latency # clock cycles in which the routers are active
            except:
                noc_utilization  = 0
                tile_utilization = 0
                
    return ( query_latency, tile_utilization, noc_utilization )

if __name__ == "__main__":
    
    for d in os.listdir("."):
        if len(sys.argv) == 2:
            assert sys.argv[1] in ["REAL","DUMB"]
            m = re.match("DSE_{}_([0-9]+)_([0-9]+)".format(sys.argv[1]),d)
        else:
            m = re.match("DSE_([0-9]+)_([0-9]+)",d)
        if m:
            #print m.groups()
            width = int(m.groups()[0])
            depth = int(m.groups()[1])
            area  = width * depth * dbmesh_core_area
            latencies, tile_cycles, router_cycles = get_latencies(d)
            if latencies is not None:
                latency = sum(latencies) * float( 1.0 / float(freq * 1000) ) # normalize to ms instead of sec
                if latency == 0:
                    continue
                    #pdb.set_trace()
                if all([x>0 for x in tile_cycles]): # in some cases I re-ran a feq queries
                    router_utilization = float(sum(router_cycles)) / sum(latencies)
                    tile_utilization   = float(sum(tile_cycles)) / sum(latencies)
                    assert router_utilization < width*depth
                    assert tile_utilization < width * depth
                else:
                    router_utilization = 0
                    tile_utilization   = 0
                    
                static_compute_pwr = width*depth*dbmesh_static_pwr
                dyn_compute_pwr    = dbmesh_dynamic_pwr * tile_utilization
                static_comm_pwr    = width*depth*router_static_pwr
                dynamic_comm_pwr   = router_utilization * router_dynamic_pwr
                
                print "{:>2} {:>2} {:>.2f} {} {} {} {} {} {} {}".format(width, depth, area, latency,
                                                                        tile_utilization,router_utilization,
                                                                        static_compute_pwr, dyn_compute_pwr, static_comm_pwr, dynamic_comm_pwr)
