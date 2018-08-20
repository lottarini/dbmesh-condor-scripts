#!/bin/bash
# this script estimates the area of a dbemsh device of width $1 and height $2
echo "$1 * $2 * (36897.120848 + 12111.1203)/1000000" | bc
