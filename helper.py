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

def cli_options(msg):
    global verbose
    parser = argparse.ArgumentParser(description=msg)
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

    helper.translate = translate
    helper.ITEMS = ITEMS
    return args.good, args.bad

def process_good_jobs(good, bad, get_nodes_in_job):
    items_in_good_jobs = []
    current_item = 0
    str_todo = "/" + str(len(good)) + " good jobs and 0/" + str(len(bad)) + " bad jobs."
    for jobid in good:
        current_item += 1
        items_in_good_jobs.append(map(translate, get_nodes_in_job(jobid)))
        log("Processed " + str(current_item) + str_todo)
    return items_in_good_jobs

def process_bad_jobs(good, bad, get_nodes_in_job):
    items_in_bad_jobs = []
    current_item = 0
    str_done = str(len(good)) + "/" + str(len(good)) + " good jobs and "
    str_todo = "/" + str(len(bad)) + " bad jobs."
    for jobid in bad:
        current_item += 1
        items_in_bad_jobs.append(map(translate, get_nodes_in_job(jobid)))
        log("Processed " + str_done + str(current_item) + str_todo)
    return items_in_bad_jobs

def other_stuff(bad):
    potential_bad_items = count_bad_items(items_in_bad_jobs)
    bad_items = remove_good_items(potential_bad_items, items_in_good_jobs)
    # transform the dict in list of tuples, sort on the index 1 (the number of times the item occurred in a bad job) starting form higher counts
    bad_item_list = bad_items.items()
    bad_item_list.sort(key=lambda element: element[1], reverse=True)

    current = len(bad) + 1
    bad_count = 0
    for bad_item in bad_item_list:
        if bad_item[1] < current:
            if bad_count > 0:
                print "\nFor a total of " + str(bad_count) + " " + ITEMS.lower()
                bad_count = 0
            current = bad_item[1]
            if current == len(bad):
                n = "all"
            else:
                n = str(current)
            print "\n" + ITEMS + " occurring in", n, "bad jobs, but none of the good jobs:"
        print bad_item[0],
        bad_count = bad_count + 1
    print "\nFor a total of " + str(bad_count) + " " + ITEMS.lower()
    print "\nFor a grand total of " + str(len(bad_item_list)) + " " + ITEMS.lower()

    if len(bad_item_list) == 0:
        print "No obvious bad " + ITEMS.lower() + " found"

