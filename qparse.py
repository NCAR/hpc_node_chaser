#!/usr/bin/env python
import os, subprocess, re, shlex
from datetime import datetime, timedelta
import helper as h

# system constants
pbslog_path = "/gpfs/pbs/server_priv/accounting/"
syslog_path = "/ssg/logs/syslog/"
log_prefix	= "chmgt."
log_start	= datetime(2016, 12, 10)
afdate_fmt = "%Y%m%d"

# Operational constants
time_vars	= ["ctime","qtime","etime","start","end"]
one_day		= timedelta(days = 1)
one_minute	= timedelta(minutes = 1)
one_sec = timedelta(seconds = 1)

def _get_nodes_in_stringIO(data, id="<unknown ID>"):
    """Parse a file or stringIO object in the tracejob format
    and return the list of nodes. It is useful to pass data
    and open filename in the invocation so this can be tested
    with plain strings instead of files."""
    h.log("Parsing...")
    group_of_nodes = []
    for line in data:
        if "exec_vnode=" in line:
            nodes = []
            stuff = line.split()
            for entry in stuff:
                if entry.startswith("exec_vnode="):          # exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36)
                    pbs_nodes = entry.split("=(")[1]         #             r10i1n26:ncpus=36)+(r10i1n31:ncpus=36)
                    pbs_node_list = pbs_nodes.split(")+(")   #             r10i1n26:ncpus=36 , r10i1n31:ncpus=36)
                    for n in pbs_node_list:
                        nodes.append(n.split(":")[0])        #             r10i1n26          , r10i1n31
            group_of_nodes.append(nodes)

    tbr = []
    for group in group_of_nodes:
        if group not in tbr:
            tbr.append(group)
    if len(tbr) > 1:
        print "WARNING: job", id, "ran", len(tbr), "times"
    h.log("Parsing completed")
    return tbr

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


def run_cmd(args):
	args 		= [str(item) for item in args]
	proc 		= subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	out_data 	= proc.communicate()[0]
	return proc.returncode, out_data

def get_job_info(job_id):
	target 		= "\;[Q,S,R,E]\;{}".format(job_id)
	cur_date	= datetime.today()
	trace_text	= []
	keep_going  = True

	print "Searching for job {} in PBS accounting logs ...".format(job_id)

	while keep_going:
		log_file		= pbslog_path + datetime.strftime(cur_date, afdate_fmt)
		status, log_data 	= run_cmd(["grep", "-a", target, log_file])

		if status == 0:
			trace_text	= log_data.splitlines() + trace_text

		cur_date 	-= 	one_day
		keep_going 	= 	(cur_date >= log_start) and (len(trace_text) < 3
						or not (";Q;" in trace_text[0]))

	if status != 0:
		print "Fatal: job {} not found in PBS logs; exiting".format(job_id)
		sys.exit(1)
	else:
		full_id	= trace_text[0].split(';')[2]
		print "Job found in PBS logs with id {}".format(full_id)

	print line
	return full_id, [shlex.split(line.replace(';', ' ', 3)) for line in trace_text]

def get_nodes_in_job(jobid):
    """Wrapper facade around the tracejob invocation logic and
    output parser. Simply return the list of nodes
    where a given jobID ran."""
    h.log("\n---------------------------------------\nProcessing job " + str(jobid))
    try:
        #nodes = _get_nodes_in_stringIO(open(_invoke_tracejob(jobid)), id=jobid)
        nodes = _get_nodes_in_stringIO(open(get_job_info(jobid)), id=jobid)
    except Exception as e:
        print e, "in job ID", jobid
        nodes = []
    h.log("Ended processing job " + str(jobid) + ", " + str(len(nodes)) + " nodes found.")
    return nodes

if __name__ == '__main__':
    h.run(help_msg = "PBS helper to find bad performing nodes or switches from a list of good and bad PBS jobs",
          get_nodes_in_job = get_nodes_in_job)

