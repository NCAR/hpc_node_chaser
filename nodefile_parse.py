#!/usr/bin/env python
import sys
# from __future__ import with_statement
import helper as h

def parse(data):
    nodes = []
    for line in data:
        linenodes = line.split(",")
        for n in linenodes:
            node = n.strip()
            if len(node) > 0:
                nodes.append(node)
    return [nodes,]

def get_nodes_in_file(filename):
    h.log("\n---------------------------------------\nProcessing file " + str(filename))
    try:
        with open(filename) as f:
            nodes = parse(f)
    except IOError as ioe:
        print ioe
        sys.exit(1)
    h.log("Ended processing file " + str(filename) + ", " + str(len(nodes)) + " nodes found.")
    return nodes

if __name__ == '__main__':
    h.run(help_msg = "Find bad performing nodes from a list of good and bad files",
          get_nodes_in_job = get_nodes_in_file, expected_type=str)

