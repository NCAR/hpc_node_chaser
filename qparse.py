#!/usr/bin/env python
import os, subprocess, re
import helper as h

def _get_nodes_in_stringIO(data):
    """Parse a file or stringIO object in the tracejob format
    and return the list of nodes. It is useful to pass data
    and open filename in the invocation so this can be tested
    with plain strings instead of files."""
    h.log("Parsing...")
    nodes = []
    for line in data:
        if "exec_vnode=" in line:
            stuff = line.split()
            for entry in stuff:
                if entry.startswith("exec_vnode="):          # exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36)
                    pbs_nodes = entry.split("=(")[1]         #             r10i1n26:ncpus=36)+(r10i1n31:ncpus=36)
                    pbs_node_list = pbs_nodes.split(")+(")   #             r10i1n26:ncpus=36 , r10i1n31:ncpus=36)
                    for n in pbs_node_list:
                        nodes.append(n.split(":")[0])        #             r10i1n26          , r10i1n31
    h.log("Parsing completed")
    return nodes

def _invoke_tracejob(jobid):
    """Invoke tracejob for a specific jobid. TBD if storing the
    output in a temporary file will be useful, but doing it
    for now"""
    name = "tracejob." + str(jobid) + ".txt"
    fullname = h.TMPDIR + name
    ALL_FILES = os.listdir(h.TMPDIR)
    if not name in ALL_FILES:
        command = "tracejob -n 50 " + str(jobid) + " > " + fullname
        h.log("Invoking: " + command)
        subprocess.call(command, shell=True)
    else:
        h.log("No need to invoke tracejob. Using cached " + fullname)
    return fullname

def get_nodes_in_job(jobid):
    """Wrapper facade around the bhist invocation logic and
    output parser. Simply return the list of nodes
    where a given jobID ran."""
    h.log("\n---------------------------------------\nProcessing job " + str(jobid))
    nodes = _get_nodes_in_stringIO(open(_invoke_tracejob(jobid)))
    h.log("Ended processing job " + str(jobid) + ", " + str(len(nodes)) + " nodes found.")
    return nodes

if __name__ == '__main__':
    h.run(help_msg = "PBS helper to find bad performing nodes or switches from a list of good and bad PBS jobs",
          get_nodes_in_job = get_nodes_in_job)

