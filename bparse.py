import os, subprocess

try:
    TMPDIR=os.environ['TMPDIR']
except KeyError:
    TMPDIR="/glade/scratch/" + os.environ['USER'] + "/.bparse/"

try: 
    os.mkdir(TMPDIR)
except OSError:
    pass # already exists

def log(string):
    if verbose:
        print string

def invoke_bhist(jobid):
    name = "bhist." + str(jobid) + ".txt"
    ALL_FILES = os.listdir(TMPDIR)
    if not name in ALL_FILES:
        command = "bhist -n 0 -l " + str(jobid) + " > " + TMPDIR + name
        log("Will invoke: " + command)
        subprocess.call(command, shell=True)
    else:
        log("Nothing to do: " + TMPDIR + name + " already there")

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('integers', metavar='jobID', type=int, nargs='+', help='IDs of the jobs to be considered')
    parser.add_argument("-c", "--common-nodes", help="Find the set of common nodes among the specified jobs", action="store_true")
    args = parser.parse_args()

    for jobid in args.integers:
        invoke_bhist(jobid)
 
