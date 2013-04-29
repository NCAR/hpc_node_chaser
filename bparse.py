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

def _get_nodes_in_stringIO(data):
    """Parse a file or stringIO object in the bhist format
    and return the list of nodes. It is useful to pass data
    and open filename in the invocation so this can be tested
    with plain strings instead of files."""
    nodes=[]
    for line in data:
        pass
    return nodes

def get_nodes_in_job(jobid):
    """Wrapper facade around the bhist invocation logic and
    bhist output parser. Simply return the list of nodes
    where a given jobID ran."""
    return _get_nodes_in_stringIO(open(_invoke_bhist(jobid)))

def _invoke_bhist(jobid):
    """Invoke bhist for a specific jobid and store the
    output in a temporary file. It's useful to cache the output in
    a file instead to process it, because bhist usually takes a long 
    time to respond and repeated invocations are likely while 
    investigating a problem. This function returns the full path
    of the file containing the bhist output."""
    name = "bhist." + str(jobid) + ".txt"
    fullname = TMPDIR + name
    ALL_FILES = os.listdir(TMPDIR)
    if not name in ALL_FILES:
        command = "bhist -n 0 -l " + str(jobid) + " > " + fullname
        log("Invoking: " + command)
        subprocess.call(command, shell=True)
    else:
        log("Nothing to do: " + fullname + " is already there")
    return fullname

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LSF helper to find bad performing nodes from a list of good and bad LSF job")
    g=parser.add_argument("--good", metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered good")
    b=parser.add_argument("--bad",  metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered bad")
    v=parser.add_argument("--verbose", help="Verbosely print messages about everything", action="store_true")
    #parser.add_argument("-c", "--common-nodes", help="Find the set of common nodes among the specified jobs", action="store_true")
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
        nodes_in_good_jobs.append(get_nodes_in_job(jobid))
 
    for jobid in args.bad:
        nodes_in_bad_jobs.append(get_nodes_in_job(jobid))

