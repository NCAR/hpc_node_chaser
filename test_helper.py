import helper

# no need to test run()

def test_process_jobs_two_nodes():
    jobs = [1234, 5678, 9101112]
    helper.translate = lambda x: x
    func = lambda x: [[str(x) + "-ib1", str(x) + "-ib2"]]
    actual = helper.process_jobs(jobs, get_nodes_in_job=func)
    expected = [[   "1234-ib1",    "1234-ib2"],
                [   "5678-ib1",    "5678-ib2"],
                ["9101112-ib1", "9101112-ib2"]]
    assert actual == expected

def test_process_jobs_one_node():
    jobs = [3875, 4960, 7258]
    helper.translate = lambda x: x
    func = lambda x: [[str(x) + "-ib1"]]
    actual = helper.process_jobs(jobs, get_nodes_in_job=func)
    expected = [["3875-ib1"],
                ["4960-ib1"],
                ["7258-ib1"]]
    assert actual == expected

def test_process_jobs_when_repeated_by_PBS():
    jobs = [929324, 932534, 942406, 943425, 936612, 943656, 943571]
    helper.translate = lambda x: x
    func = lambda x: ([str(x) + "-1st_node-1st_run", str(x) + "-2nd_node-1st_run"], [str(x) + "-1st_node-2nd_run", str(x) + "-2nd_node-2nd_run"])
    actual = helper.process_jobs(jobs, get_nodes_in_job=func)
    expected = [["929324-1st_node-1st_run", "929324-2nd_node-1st_run"],
                ["929324-1st_node-2nd_run", "929324-2nd_node-2nd_run"],
                ["932534-1st_node-1st_run", "932534-2nd_node-1st_run"],
                ["932534-1st_node-2nd_run", "932534-2nd_node-2nd_run"],
                ["942406-1st_node-1st_run", "942406-2nd_node-1st_run"],
                ["942406-1st_node-2nd_run", "942406-2nd_node-2nd_run"],
                ["943425-1st_node-1st_run", "943425-2nd_node-1st_run"],
                ["943425-1st_node-2nd_run", "943425-2nd_node-2nd_run"],
                ["936612-1st_node-1st_run", "936612-2nd_node-1st_run"],
                ["936612-1st_node-2nd_run", "936612-2nd_node-2nd_run"],
                ["943656-1st_node-1st_run", "943656-2nd_node-1st_run"],
                ["943656-1st_node-2nd_run", "943656-2nd_node-2nd_run"],
                ["943571-1st_node-1st_run", "943571-2nd_node-1st_run"],
                ["943571-1st_node-2nd_run", "943571-2nd_node-2nd_run"]]
    assert actual == expected

def test_find_bad_nodes():
    assert False, "test not implemented yet"

def test_count_bad_nodes():
    # repeated nodes in different jobs must be counted repeatedly
    # there can't be repeated nodes
    list_of_lists = [["A", "B", "C"], ["B", "C", "D"]]
    expected = {"A": 1, "B": 2, "C": 2, "D": 1 }
    actual = helper.count_bad_items(list_of_lists)
    assert actual == expected

def test_count_bad_switches():
    # repeated switches in same job must not be counted repeatedly
    list_of_lists = [["A", "B", "B", "B", "C"], ["B", "B", "C", "C", "D"]]
    expected = {"A": 1, "B": 2, "C": 2, "D": 1 }
    actual = helper.count_bad_items(list_of_lists)
    assert actual == expected

def test_remove_good_items():
    potential_bad_list = {"A": 1, "B": 2, "C": 2, "D": 1 }
    list_of_lists = [["B","F"],["D","E"]]
    expected = {"A": 1, "C": 2}
    actual = helper.remove_good_items(potential_bad_list, list_of_lists)
    assert actual == expected
