import helper

# no need to test run

def test_process_good_jobs():
    assert False, "test not implemented yet"

def test_process_bad_jobs():
    assert False, "test not implemented yet"

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
