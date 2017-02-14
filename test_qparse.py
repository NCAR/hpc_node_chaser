import qparse
import cStringIO, pytest

def test_get_nodes_in_stringIO_empty():
    s=cStringIO.StringIO("""nothing to be found here""")
    expected = []
    nodes=qparse._get_nodes_in_stringIO(s)
    assert nodes == expected

def test_get_nodes_in_stringIO_single():
    s=cStringIO.StringIO("""
02/09/2017 07:54:27  A    queue=regular
02/09/2017 14:27:16  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n31/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 resource_assigned.mem=15774144000kb resource_assigned.ncpus=17280
    """)

    expected = ["r10i1n26", "r10i1n31"]
    nodes=qparse._get_nodes_in_stringIO(s)
    assert nodes == expected

def test_get_nodes_in_stringIO_multiple_identical():
    s=cStringIO.StringIO("""
02/09/2017 07:54:27  A    queue=regular
02/09/2017 14:27:16  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n31/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 resource_assigned.mem=15774144000kb resource_assigned.ncpus=17280
02/09/2017 14:27:50  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n31/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 session=0 end=1486675670 Exit_status=-2 resources_used.cpupercent=0 resources_used.cput=00:00:00 resources_used.mem=0kb resources_used.ncpus=8640 resources_used.vmem=0kb resources_used.walltime=00:00:00 run_count=1
02/09/2017 14:27:50  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n31/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 session=0 end=1486675670 Exit_status=-2 resources_used.cpupercent=0 resources_used.cput=00:00:00 resources_used.mem=0kb resources_used.ncpus=8640 resources_used.vmem=0kb resources_used.walltime=00:00:00 run_count=1
    """)

    expected = ["r10i1n26", "r10i1n31"]
    nodes=qparse._get_nodes_in_stringIO(s)
    assert nodes == expected

def test_get_nodes_in_stringIO_multiple_different():
    s=cStringIO.StringIO("""
02/09/2017 07:54:27  A    queue=regular
02/09/2017 14:27:16  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n24/0*36+r10i1n31/0*36 exec_vnode=(r10i1n24:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 resource_assigned.mem=15774144000kb resource_assigned.ncpus=17280
02/09/2017 14:27:50  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n31/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n31:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 session=0 end=1486675670 Exit_status=-2 resources_used.cpupercent=0 resources_used.cput=00:00:00 resources_used.mem=0kb resources_used.ncpus=8640 resources_used.vmem=0kb resources_used.walltime=00:00:00 run_count=1
02/09/2017 14:27:50  A    user=jimenez group=ncar account="ARAL0001" project=_pbs_project_default jobname=WRF_100 queue=regular ctime=1486652067 qtime=1486652067 etime=1486652067 start=1486675636 exec_host=r10i1n26/0*36+r10i1n34/0*36 exec_vnode=(r10i1n26:ncpus=36)+(r10i1n34:ncpus=36) Resource_List.mpiprocs=8640 Resource_List.ncpus=8640 Resource_List.nodect=240 Resource_List.place=scatter:exclhost Resource_List.select=240:mpiprocs=36 Resource_List.walltime=10:00:00 session=0 end=1486675670 Exit_status=-2 resources_used.cpupercent=0 resources_used.cput=00:00:00 resources_used.mem=0kb resources_used.ncpus=8640 resources_used.vmem=0kb resources_used.walltime=00:00:00 run_count=1
    """)

    with pytest.raises(Exception):
        nodes=qparse._get_nodes_in_stringIO(s)
