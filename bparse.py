import sys, os, subprocess

verbose=False
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

def node_in_job(jobid):
    return []

def invoke_bhist(jobid):
    """Invoke bhist for a specific jobid and store the
    output in a temporary file. It's useful to cache since
    bhist usually takes long to respond and repeated invocations
    are likely while investigating a problem"""
    name = "bhist." + str(jobid) + ".txt"
    ALL_FILES = os.listdir(TMPDIR)
    if not name in ALL_FILES:
        command = "bhist -n 0 -l " + str(jobid) + " > " + TMPDIR + name
        log("Invoking: " + command)
        subprocess.call(command, shell=True)
    else:
        log("Nothing to do: " + TMPDIR + name + " is already there")

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LSF helper to find bad performing nodes from a list of good and bad LSF job")
    g=parser.add_argument("--good", metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered good")
    b=parser.add_argument("--bad",  metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered bad")
    v=parser.add_argument("--verbose", help="Verbosely print messages about everything", action="store_true")
    args = parser.parse_args()

    if not args.bad:
        args.bad=[]
    if not args.good:
        args.good=[]
    if len(args.bad) + len(args.good) == 0:
        print "No jobs specified, nothing to do"
        parser.print_usage()
        sys.exit(2)
    if args.verbose:
        verbose = True
        log(v.help)

    nodes_in_good_jobs =  []
    nodes_in_bad_jobs =  []
    for jobid in args.good:
        invoke_bhist(jobid)
        nodes_in_good_jobs.append(node_in_job(jobid))
 
    for jobid in args.bad:
        invoke_bhist(jobid)
        nodes_in_bad_jobs.append(node_in_job(jobid))

