#!/bin/bash
python gather.py DUMB > dbmesh.dumb.tsmc.out
python gather.py > dbmesh.ideal.tsmc.out
# this is done last so that the area stats are about useful things
python gather.py REAL > dbmesh.real.tsmc.out
