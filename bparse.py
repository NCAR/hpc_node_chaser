#!/bin/env python
import sys, os, subprocess
import re

verbose=False
try:
    TMPDIR=os.environ['TMPDIR'] + "/.bparse/"
except KeyError:
    TMPDIR="/glade/scratch/" + os.environ['USER'] + "/.bparse/"
try: 
    os.mkdir(TMPDIR)
except OSError:
    pass # already exists

try:
    CONFDIR=os.environ['BPARSEDIR']
except KeyError:
    CONFDIR=os.environ['HOME'] + "/.bparse/"
sys.path.append(CONFDIR)

start_regex = re.compile(r".+: Dispatched to \d+ Hosts/Processors ")
node_regex = re.compile(r"""<           # start of the pattern
                              \d+       # number of tasks on that node
                              \*        # literal star '*'
                              (         # ---- capture as \1
                              .*?       # name of the node (anything) 
                              )         # ---- end of capture
                                        # note '*' is greedy and would match as much as possible,
                                        # whereas here we want to much as little as possible and
                                        # therefore we use the modified '*?' variant
                              >         # end of the pattern""", re.VERBOSE) 

def log(string):
    if verbose:
        print string

def _get_nodes_in_stringIO(data):
    """Parse a file or stringIO object in the bhist format
    and return the list of nodes. It is useful to pass data
    and open filename in the invocation so this can be tested
    with plain strings instead of files."""
    found_start = False
    node_string_as_list=[]
    log("Parsing...")
    for line in data:
        if found_start:
            if not line.startswith(' '):              # end of node list section
                break
            node_string_as_list.append(line.strip())
            if line.endswith(';'):                    # end of node list section
                break
        else:
            match = start_regex.findall(line)
            if match:
                log("Node list section found, starting in line\n===\n" + line + "===")
                node_string_as_list.append(line.lstrip(match[0]).strip())
                found_start = True

    log("Parsing completed")
    node_string = ''.join(node_string_as_list)
    nodes = node_regex.findall(node_string)
    return nodes

def get_nodes_in_job(jobid):
    """Wrapper facade around the bhist invocation logic and
    bhist output parser. Simply return the list of nodes
    where a given jobID ran."""
    log("\n---------------------------------------\nProcessing job " + str(jobid))
    nodes = _get_nodes_in_stringIO(open(_invoke_bhist(jobid)))
    log("Ended processing job " + str(jobid) + ", " + str(len(nodes)) + " nodes found.")
    return nodes

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

from collections import defaultdict
def count_bad_items(list_of_baditem_lists):
    d = defaultdict(int)
    for baditem_list in list_of_baditem_lists:
        already_added = []
        for baditem in baditem_list:
            if not baditem in already_added:
                already_added.append(baditem)
                d[baditem] += 1
    return d

def remove_good_items(bad_items, list_of_gooditem_lists):
    for gooditem_list in list_of_gooditem_lists:
        for gooditem in gooditem_list:
            try:
                del bad_items[gooditem] # another strategy might be to decrement it instead
            except KeyError:
                pass                    # if it wasn't there, nothing to do
    return bad_items

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LSF helper to find bad performing nodes or switches from a list of good and bad LSF jobs")
    parser.add_argument("--bad",  metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered bad", required=True)
    parser.add_argument("--good", metavar="ID", type=int, nargs='+', help="LSF job IDs of the jobs to be considered good")
    parser.add_argument("--switch", metavar="<mod>", help="Translate nodes names to switch names, using python module " + CONFDIR + "<mod>.py")
    v=parser.add_argument("--verbose", help="Verbosely print messages about everything", action="store_true")
    args = parser.parse_args()

    if not args.good:
        args.good=[]
    if args.verbose:
        verbose = True
        log(v.help)

    # if a node-to-switch translation has been requested, use it
    # otherwise make a no-op translate
    if args.switch:
        log("Loading " + CONFDIR + args.switch + ".py")
        switches = __import__(args.switch)
        translate = switches.translate
        ITEMS = "Switches"
    else:
        translate = lambda x: x
        ITEMS = "Nodes"

    items_in_good_jobs = []
    items_in_bad_jobs = []
    for jobid in args.good:
        items_in_good_jobs.append(map(translate, get_nodes_in_job(jobid)))
 
    for jobid in args.bad:
        items_in_bad_jobs.append(map(translate, get_nodes_in_job(jobid)))

    potential_bad_items = count_bad_items(items_in_bad_jobs)
    bad_items = remove_good_items(potential_bad_items, items_in_good_jobs)

    # transform the dict in list of tuples, sort on the index 1 (the number of times the item occurred in a bad job) starting form higher counts
    bad_item_list = bad_items.items()
    bad_item_list.sort(key=lambda element: element[1], reverse=True)

    current = len(args.bad) + 1
    for bad_item in bad_item_list:
        if bad_item[1] < current:
            current = bad_item[1]
            if current == len(args.bad):
                n = "all"
            else:
                n = str(current)
            print "\n\n" + ITEMS + " occurring in", n, "bad jobs, but none of the good jobs:"
        print bad_item[0],

