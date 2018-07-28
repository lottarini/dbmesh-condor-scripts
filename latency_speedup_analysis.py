import os
import re
import sys
import argparse
sys.path.append(os.path.abspath('/home/lottarini/DBMESH/db-mesh/sql_compiler'))
from gather import get_latencies
import numpy as np
import matplotlib.pyplot as plt

colors = ['r','g','b']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directories",type=str, nargs="+",help="Directories containing the results")
    parser.add_argument("--labels",type=str, nargs="+",help="label for each directory dataset")
    args, extra = parser.parse_known_args()

    labels = args.labels if args.labels is not None else args.directories
    #assert len(labels) == len(args.directories)
    # create plot
    fig, ax = plt.subplots()
    bar_width = (1.0/(len(args.directories)-1) - 0.05)
    
    # x = range(22 * len(args.directories) )
    # y = [ 0 for x in range(22 * len(args.directories) ) ]
    ref_latency = get_latencies(args.directories[0])
    for j,d in enumerate(args.directories[1:]):
        assert os.path.isdir(d)

        latencies = get_latencies(d)
        plt.bar( [ 1+x+j*bar_width for x in range(22) ] ,
                     [ x/y if y != 0 else 0 for x,y in zip(ref_latency,latencies)] ,
                     bar_width, color = colors[j], label=labels[j] )
    #     for i,l in enumerate(latencies):
    #         y[i*3+j] = l

        
    # plt.bar(x,y)
    plt.xlabel('Query')
    plt.xticks(range(1,23))
    plt.ylabel('Scheduling Speedup')
    plt.legend()
    plt.tight_layout()
    plt.show()
