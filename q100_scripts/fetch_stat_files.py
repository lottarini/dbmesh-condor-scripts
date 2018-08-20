import os
import argparse
import sys
import pdb
from shutil import copyfile

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dse",type=str,help="File containing the results for pareto points")
    #parser.add_argument("input_dir",type=str,help="Folder containing all the stat files")
    parser.add_argument("output_dir",type=str,help="Folder where stat files of pareto optimal runs will be saved")
    parser.add_argument("--debug",action="store_true",help="Print list of cp commands instead of executing them")
    args = parser.parse_args()
    assert os.path.isfile(args.dse)
    #assert os.path.isdir(args.input_dir)
    assert os.path.isdir(args.output_dir)

    legend = None
    with open(args.dse) as f:
        for line in f:
            if line[0] == "#":
                legend = [s.strip() for s in line[1:].split(";")]
            else:
                assert legend is not None
                stuff = line.split(";")
                dse_uid_index = legend.index("dse_uid")
                run_indexes_index = legend.index("run_index")
                dse_uid = int(stuff[dse_uid_index])
                run_indexes =eval(stuff[run_indexes_index] )
                print dse_uid,run_indexes
                for ri in run_indexes:
                    filename = "stats.{}.{}".format(dse_uid,ri)
                    src_path = os.path.join(str(dse_uid),"dse_stats",filename)
                    dst_path = os.path.join(args.output_dir,filename)
                    assert os.path.isfile(src_path), "src path {} does not exist".format(src_path)
                    #assert not os.path.isfile(dst_path)
                    if args.debug:
                        print "cp {} {}".format(src_path,dst_path)
                    else:
                        copyfile(src_path,dst_path)
