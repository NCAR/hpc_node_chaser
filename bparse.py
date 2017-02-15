#!/usr/bin/env python
import os, subprocess, re
import helper as h

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

def _get_nodes_in_stringIO(data):
    """Parse a file or stringIO object in the bhist format
    and return the list of nodes. It is useful to pass data
    and open filename in the invocation so this can be tested
    with plain strings instead of files."""
    found_start = False
    node_string_as_list=[]
    h.log("Parsing...")
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
                h.log("Node list section found, starting in line\n===\n" + line + "===")
                node_string_as_list.append(line.lstrip(match[0]).strip())
                found_start = True

    h.log("Parsing completed")
    node_string = ''.join(node_string_as_list)
    nodes = node_regex.findall(node_string)
    return [nodes]

def _invoke_bhist(jobid):
    """Invoke bhist for a specific jobid and store the
    output in a temporary file. It's useful to cache the output in
    a file instead to process it, because bhist usually takes a long 
    time to respond and repeated invocations are likely while 
    investigating a problem. This function returns the full path
    of the file containing the bhist output."""
    name = "bhist." + str(jobid) + ".txt"
    fullname = h.TMPDIR + name
    ALL_FILES = os.listdir(h.TMPDIR)
    if not name in ALL_FILES:
        command = "bhist -n 50 -l " + str(jobid) + " > " + fullname
        h.log("Invoking: " + command)
        subprocess.call(command, shell=True)
    else:
        h.log("No need to invoke bhist. Using cached " + fullname)
    return fullname

def get_nodes_in_job(jobid):
    """Wrapper facade around the bhist invocation logic and
    bhist output parser. Simply return the list of nodes
    where a given jobID ran."""
    h.log("\n---------------------------------------\nProcessing job " + str(jobid))
    nodes = _get_nodes_in_stringIO(open(_invoke_bhist(jobid)))
    h.log("Ended processing job " + str(jobid) + ", " + str(len(nodes)) + " nodes found.")
    return nodes

if __name__ == '__main__':
    h.run(help_msg = "LSF helper to find bad performing nodes or switches from a list of good and bad LSF jobs",
          get_nodes_in_job = get_nodes_in_job)

