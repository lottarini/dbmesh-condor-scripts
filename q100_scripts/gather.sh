#!/bin/bash

rm -f dse.out
rm -rf ./pareto_stats
mkdir pareto_stats
cat $(find . -name dse.out) > dse.out
echo "All dse outputs have been concatenated"
python dse_to_pareto.py dse.out > dse.pareto.out
python fetch_stat_files.py  dse.pareto.out ./pareto_stats/
echo "outputs ready: dse.out dse.pareto.out pareto_stats"
