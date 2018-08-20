import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pdb

from compute_area_power import get_power,get_area,get_cc

#http://pythonfiddle.com/pareto-simple-cull/
def simple_cull(inputPoints, dominates):
    paretoPoints    = set()
    candidateRowNr  = 0
    dominatedPoints = set()
    while len(inputPoints):
        candidateRow = inputPoints.pop()
        nonDominated = True
        next_round   = []
        while len(inputPoints) != 0:
            row = inputPoints.pop()
            if dominates(candidateRow, row):
                dominatedPoints.add(tuple(row))
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedPoints.add(tuple(candidateRow))
                next_round.append(row)                
            else:
                next_round.append(row)
                
        if nonDominated:
            # add the non-dominated point to the Pareto frontier
            paretoPoints.add(tuple(candidateRow))
                
        # fig1, ax1 = plt.subplots()
        # x,y = zip(*dominatedPoints)
        # ax1.scatter(x,y,color ="r", marker="x")
        # if len(paretoPoints) > 0:
        #     x,y = zip(*paretoPoints)
        #     ax1.scatter(x,y,marker="p",color="g",s=16)
            
        # ax1.set_xlim([0,60000000])
        # ax1.set_ylim([0,25000000])
        # ax1.set_title("{} Points to examine {} points eliminated".format(len(next_round),len(dominatedPoints)))
        # plt.show()
        
        inputPoints = next_round
        
    return paretoPoints, dominatedPoints

def dominates(row, anotherRow):
    return all([row[x] < anotherRow[x] for x in range(len(row))])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dse",type=str,help="File containing the results of the domain space xploration")
    parser.add_argument("--power",action="store_true",help="use power as cost metric instead of area")
    args = parser.parse_args()
    
    assert os.path.isfile(args.dse)
    line_dict = {}
    points = []
    legend_found = False
    with open(args.dse) as f:
        for line in f:
            if line[0] == "#":
                if not legend_found:
                    print line.strip()
                legend_found = True
            else:
            
                tile_area, noc_area = get_area(line)
                area = tile_area + noc_area 
                latency = get_cc(line) 
                power = get_power(line) 
            
                if args.power:
                    key = ( power,latency)
                else:
                    key = ( area,latency)
                
                points.append(key)
                assert key not in line_dict
                line_dict[key] = line
                
    assert legend_found
    # fig2, ax2 = plt.subplots()
    # ax2.scatter(x,latency)
    # ax2.set_xlim([0,60000000])
    # ax2.set_ylim([0,25000000])
    # fig2.savefig('q100_points.pdf')
        
    pp,dp = simple_cull(points,dominates)
                          
    # pareto_x, pareto_y = zip(*pp)
    # fig1, ax1 = plt.subplots()
    # ax1.scatter(pareto_x,pareto_y)
    # ax1.set_xlim([0,60000000])
    # ax1.set_ylim([0,25000000])
    # fig1.savefig('q100_pareto_points.pdf')
    
    for key in pp:
        print line_dict[key].strip()
