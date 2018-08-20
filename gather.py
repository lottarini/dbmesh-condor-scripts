import os
import re
import sys
import pdb
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats
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
    freq = 950
    #old
    # router_static_pwr  = 0.000125
    # router_dynamic_pwr = 0.000308
    dbmesh_static_pwr  = 0.000611
    dbmesh_dynamic_pwr = 0.009015
    router_static_pwr  = 0.0001433
    router_dynamic_pwr = 0.00813    
else:
    raise NotImplementedError

working_queries = [1,2,3,4,5,6,7,8,9,10,11,12,14,16,17,18,19,20,22]

def get_latencies(d):
    latency = []
    noc_cycles = []
    compute_cycles = [] # this consider each PE working for the entire directive
    tile_cycles = [] # this is more precise and considers load inbalance
    for i in working_queries:
        stat_file = os.path.join(d,str(i),"stats")
        if os.path.isfile(stat_file):
            with open(stat_file) as f:
                ct, ccc, ncc, tcc = analyze_stats(f)
                    
                latency.append( ct )
                noc_cycles.append(ncc)
                tile_cycles.append(tcc)
                compute_cycles.append(ccc)
                #print "{:<4}\t{:>10}".format(i,cc)
        else:
            latency.append(0)
            noc_cycles.append(0)
            compute_cycles.append(0)
            tile_cycles.append(0)
            
    return latency, compute_cycles, noc_cycles, tile_cycles

def analyze_stats(stat_file):
    ''' Returns the completion time of the query, time spent in tiles, time spent in routers '''
    query_latency = 0

    tile_utilization = 0
    noc_utilization = 0
    tile_cycles = 0
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
                if int(values[6]) <= int(values[7]):
                    tile_utilization +=  int(values[6])  * directive_latency
                    noc_utilization  +=  ( int(values[7]) ) * directive_latency # clock cycles in which the routers are active
                else:
                    tile_utilization += 0
                    noc_utilization  += 0                    
            except:
                noc_utilization  = 0
                tile_utilization = 0
        elif (values[1] == "Tile"):
            if (len(values) >= 9):
                # multiply latency by number of tile used
                tile_cycles += int(values[4]) * float(values[8])
                
    return ( query_latency, tile_utilization, noc_utilization, tile_cycles )

if __name__ == "__main__":

    area_used = [[] for i in range(19)] # how much area is used for each query by the different systems
    area_lost_unbalance = [[] for i in range(19)] # how much area is lost by co-scheduling things with different latency
    area_lost_unused = [[] for i in range(19)] # how much area is not necessary
    area_perf_by_query = []
    power_perf_by_query = []
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
            latencies, tile_cycles, router_cycles, tile_precise_cycles = get_latencies(d)

            for i in range(len(tile_precise_cycles)):
                if latencies[i] > 0 and tile_precise_cycles[i] > 0:
                    area_used[i].append(tile_precise_cycles[i]/(float(width*depth)*latencies[i]))
                    try:
                        assert tile_cycles[i] >= tile_precise_cycles[i]
                    except:
                        pdb.set_trace()
                    area_lost_unbalance[i].append( (tile_cycles[i]-tile_precise_cycles[i]) / (float(width*depth)*latencies[i]) )
                    area_lost_unused[i].append( ( (float(width*depth)*latencies[i]) - tile_cycles[i]) / (float(width*depth)*latencies[i]) )

            if latencies is not None and 0 not in latencies:
                area_perf_by_query.append([area]+[ x* float( 1.0 / float(freq * 1000) ) for x in latencies])
                cc_geomean = scipy.stats.gmean(latencies)
                geomean = cc_geomean * float( 1.0 / float(freq * 1000) )
                latency = sum(latencies) * float( 1.0 / float(freq * 1000) ) # normalize to ms instead of sec
                if latency == 0:
                    continue
                    #pdb.set_trace()
                    
                if all([ x > 0 for x in tile_precise_cycles ]): # in some cases I re-ran a few queries so not all have utilization info
                    router_utilization = float(sum(router_cycles)) / sum(latencies)
                    #tile_utilization   = float(sum(tile_precise_cycles)) / sum(latencies)
                    tile_utilization = float(sum(tile_precise_cycles)) / sum(latencies)

                    assert router_utilization < width*depth
                    assert tile_utilization < width * depth
                    static_compute_pwr = width*depth*dbmesh_static_pwr
                    dyn_compute_pwr    = dbmesh_dynamic_pwr * tile_utilization
                    static_comm_pwr    = width*depth*router_static_pwr
                    dynamic_comm_pwr   = router_utilization * router_dynamic_pwr
                    total_pwr = static_compute_pwr + dyn_compute_pwr + static_comm_pwr + dynamic_comm_pwr
                    power_perf_by_query.append([total_pwr]+[ x* float( 1.0 / float(freq * 1000) ) for x in latencies])
                else:
                    router_utilization = 0
                    tile_utilization   = 0

                    static_compute_pwr = 0
                    dyn_compute_pwr    = 0
                    static_comm_pwr    = 0
                    dynamic_comm_pwr   = 0

                                    
                print "{:>2} {:>2} {:>.2f} {} {} {} {} {} {} {} {}".format(width, depth, area, latency,
                                                                        tile_utilization,router_utilization,
                                                                        static_compute_pwr, dyn_compute_pwr, static_comm_pwr, dynamic_comm_pwr, geomean)

    fig,ax = plt.subplots()
    ax.boxplot(area_used)
    ax.set_ylabel('Average DbMesh Area Used')
    ax.set_xlabel('Queries')
    ax.set_ylim([0,1])
    fig.savefig("dbmesh_area_used.pdf")

    fig1,ax1 = plt.subplots()
    ax1.boxplot(area_lost_unbalance)
    ax1.set_ylabel('DbMesh Area unused due to load imbalance')
    ax1.set_xlabel('Queries')
    ax1.set_ylim([0,1])
    fig1.savefig("dbmesh_area_lost_unbalance.pdf")

    fig2,ax2 = plt.subplots()
    ax2.boxplot(area_lost_unused)
    ax2.set_ylabel('DbMesh Area due to inutilization')
    ax2.set_xlabel('Queries')
    ax2.set_ylim([0,1])
    fig2.savefig("dbmesh_area_lost_unused.pdf")

    # DUMP THE BY-QUERY DATA
    with open("dbmesh.area.perf.byquery.csv",'w') as f:
        for row in area_perf_by_query:
            f.write(",".join([str(x) for x in row])+"\n")
    with open("dbmesh.power.perf.byquery.csv",'w') as f:
        for row in power_perf_by_query:
            f.write(",".join([str(x) for x in row])+"\n")
    
    
    # DUMP THE CSV
    csvs = {"dbmesh_area_lost_unused.csv":area_lost_unused,
                "dbmesh_area_used.csv":area_used,
            "dbmesh_area_lost_unbalance.csv":area_lost_unbalance
                }
    
    for k,v in csvs.items():
        with open(k,'w') as f:
            for query_data in v:
                f.write(",".join([str(x) for x in query_data])+"\n")

                                                   
