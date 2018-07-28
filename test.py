import sys
import os
import argparse
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler/tools'))
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler'))
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh'))

from utilization import analyze_stats
from gather import get_latencies
import numpy as np
import matplotlib.pyplot as plt
import re
import pdb

def succesful(out_file):
    line = ""
    with open(out_file) as f:
        for line in f:
            pass
        
    return "SUCCESS" in line

colors = ['r','g','b']
markers = ['o','*','d']

def get_tiles_used(stat_file):
    ''' Given an opened stat file extract the number of tiles used per directive 

    Returns:
    	a # directives long list of utilization
    '''
    tiles_used = []
    with open(stat_file) as f:
        for stat_line in f:
            if re.search("Area",stat_line):
                continue
            values = stat_line.split(",")
            if (values[1] == "DIRECTIVE"):                            
                tiles_used.append(float(values[6]))
            
    return tiles_used

def get_directive_latencies(stat_file):
    ''' Given an opened stat file extract the latency of a directive 

    Returns:
    	a # directives long list of tiles used
    '''
    ideal_directive_latencies = []
    with open(stat_file) as f:
        for stat_line in f:
            if re.search("Area",stat_line):
                continue
            values = stat_line.split(",")
            if (values[1] == "DIRECTIVE"):                            
                ideal_directive_latencies.append(float(values[2]))
                
    return ideal_directive_latencies

def get_inst_per_directive(stat_file):
    inst_per_directive = []
    inst_count = 0
    with open(stat_file) as f:
        for stat_line in f:
            if re.search("Area",stat_line):
                continue
            values = stat_line.split(",")
            if (values[1] == "Tile"):
                inst_count += 1
            if (values[1] == "DIRECTIVE"):
                inst_per_directive.append(inst_count)
                inst_count = 0

    return inst_per_directive

def get_utilization(d, width, height):
    out = []
    print "\n",d
    for i in range(1,23):
        ideal_directive_latency = []
        tiles_used   = []

        out_file  = os.path.join(d,str(i),"main.out")
        stat_file = os.path.join(d,str(i),"stats")
        if os.path.isfile(out_file) and os.path.isfile(stat_file) and succesful(out_file):
            ideal_directive_latency = get_directive_latencies(stat_file)
            tiles_used = get_tiles_used(stat_file)
            insts_used = get_inst_per_directive(stat_file)
            # with open(stat_file) as f:
            #     for stat_line in f:
            #         if re.search("Area",stat_line):
            #             continue
            #         values = stat_line.split(",")
            #         if (values[1] == "DIRECTIVE"):                            
            #             tiles_used.append(float(values[-2]))
            #             #ideal_directive_latency.append(float(values[2]))
                        
            total_latency = sum(ideal_directive_latency)
            max_utilization = float(width) * float(height)
            dir_utilization = [ x / max_utilization for x in tiles_used ]
            
            # summation over all directives
            utilization = sum([ u * ( v / total_latency ) for u,v in zip(dir_utilization, ideal_directive_latency)] )
            print i,dir_utilization,utilization
            out.append( utilization )
        else:
            out.append(0)
            
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("width",type=int)
    parser.add_argument("height",type=int)

    parser.add_argument("directories",type=str, nargs="+",help="Directories containing the results")
    parser.add_argument("--labels",type=str, nargs="+",help="label for each directory dataset")
    args, extra = parser.parse_known_args()
    
    labels = args.labels if args.labels is not None else args.directories
    #assert len(labels) == len(args.directories)
    # create plot
    fig, ax = plt.subplots()
    bar_width = (1.0/(len(args.directories)-1) - 0.05)

    ref_latency = get_latencies(args.directories[0])
    ref_utilization = get_utilization(args.directories[0],args.width,args.height)
    for j,d in enumerate(args.directories[1:]):
        assert os.path.isdir(d)

        latencies   = get_latencies(d)
        utilization = get_utilization(d,args.width,args.height)
       
        # plt.scatter( utilization , [ x/y if y != 0 else 0 for x,y in zip(ref_latency,latencies)] , color = colors[j], label=labels[j] , marker=markers[j])
        plt.scatter( [ x/y if y != 0 else 0 for x,y in zip(utilization,ref_utilization)] , [ x/y if y != 0 else 0 for x,y in zip(ref_latency,latencies)] , color = colors[j], label=labels[j] , marker=markers[j])

    plt.ylabel('Speedup over Serial')
    plt.xlabel('Utilization Speedup over Serial')
    plt.legend()
    plt.tight_layout()
    plt.ylim(ymin=0)
    plt.axvline(x=1)
    plt.axhline(y=1)

    fig.savefig('normalized_speedup.png')
