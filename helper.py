#!/usr/bin/env python
import sys, os, argparse
import helper # itself, to add fields to its dict

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

def log(string):
    if verbose:
        print string

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

def run(help_msg = None, get_nodes_in_job = None, expected_type=int):
    global verbose
    parser = argparse.ArgumentParser(description = help_msg)
    parser.add_argument("--bad",  metavar="ID", type=expected_type, nargs='+', help="Job IDs of the jobs to be considered bad", required=True)
    parser.add_argument("--good", metavar="ID", type=expected_type, nargs='+', help="Job IDs of the jobs to be considered good")
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

    helper.translate = translate
    helper.ITEMS = ITEMS

    msg = "/" + str(len(args.good)) + " good jobs and 0/" + str(len(args.bad)) + " bad jobs."
    items_in_good_jobs = process_jobs(jobs = args.good,
                                      msg_tail = msg,
                                      get_nodes_in_job=get_nodes_in_job)

    msg_head = str(len(args.good)) + "/" + str(len(args.good)) + " good jobs and "
    msg_tail = "/" + str(len(args.bad)) + " bad jobs."
    items_in_bad_jobs =  process_jobs(jobs = args.bad,
                                      msg_head = msg_head,
                                      msg_tail = msg_tail,
                                      get_nodes_in_job=get_nodes_in_job)
    find_bad_nodes(items_in_good_jobs, items_in_bad_jobs, args.bad)

def process_jobs(jobs=None, msg_head="", msg_tail="", get_nodes_in_job=None):
    items_in_jobs = []
    current_item = 0
    for jobid in jobs:
        current_item += 1
        items_in_jobs.extend(map(translate, get_nodes_in_job(jobid)))
        log("Processed " + msg_head + str(current_item) + msg_tail)
    return items_in_jobs

def find_bad_nodes(items_in_good_jobs, items_in_bad_jobs, bad):
    potential_bad_items = count_bad_items(items_in_bad_jobs)
    bad_items = remove_good_items(potential_bad_items, items_in_good_jobs)
    # transform the dict in list of tuples, sort on the index 1 (the number of times the item occurred in a bad job) starting form higher counts
    bad_item_list = bad_items.items()
    bad_item_list.sort(key=lambda element: element[1], reverse=True)

    #current = len(bad) + 1
    current = len(items_in_bad_jobs) + 1
    log("DEBUG: compare " + str(len(bad) + 1) + " and " + str(len(items_in_bad_jobs) + 1))
    print "Considering", current - 1,  "runs (some might have run more than once)"
    bad_count = 0
    for bad_item in bad_item_list:
        if bad_item[1] < current:
            if bad_count > 0:
                print "\nFor a total of " + str(bad_count) + " " + ITEMS.lower()
                bad_count = 0
            current = bad_item[1]
            print "\n" + ITEMS + " occurring in", current, "bad runs, but none of the good runs:"
        print bad_item[0],
        bad_count = bad_count + 1
    print "\nFor a total of " + str(bad_count) + " " + ITEMS.lower()
    print "\nFor a grand total of " + str(len(bad_item_list)) + " " + ITEMS.lower()

    if len(bad_item_list) == 0:
        print "No obvious bad " + ITEMS.lower() + " found"

