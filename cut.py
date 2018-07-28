import sys

with open(sys.argv[1]) as f:
    for line in f:
        stuff = line.split()
        integer = stuff[-1].split(".")[0]

        print "\t".join(stuff[:-1]),integer
