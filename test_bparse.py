import bparse
import cStringIO

def test_get_nodes_in_stringIO():
    s=cStringIO.StringIO("""
This text at the beginning must be ignored
Wed Apr 24 14:30:03 2012: Submitted from host <be1234-ib>, to Queue <economy>
Sat Apr 20 03:48:51 2012: Dispatched to 16384 Hosts/Processors <16*be3769-ib> <
                          16*be3770-ib> <16*be3771-ib> <16*be3772-ib> <16*be380
                          1-ib> <16*be3802-ib> <16*be3803-ib> <16*be3804-ib> <1
                          6*be3805-ib> <16*be3806-ib> <16*be3807-ib> <16*be3808
                          -ib> <16*be3809-ib> <16*be3810-ib> <16*be3811-ib> <16
                          *be3812-ib> <16*be3813-ib> <16*be3814-ib> <16*be3815-
                          ib> <16*be3816-ib> <16*be3817-ib> <16*be3818-ib> <16*
                          be3819-ib> <16*be3820-ib> <16*be3821-ib> 
Fri Apr 19 02:07:32 2012: Starting (Pid 22545);
                          By chance mention of <16*be6352-ib>
    """)
    # note that be6352-ib is mentioned by chance and should not be in the expected list
    # note the same is true for be1234-ib
    expected = ["be3769-ib", "be3770-ib", "be3771-ib", "be3772-ib", "be3801-ib", 
    "be3802-ib", "be3803-ib", "be3804-ib", "be3805-ib", "be3806-ib", "be3807-ib", 
    "be3808-ib", "be3809-ib", "be3810-ib", "be3811-ib", "be3812-ib", "be3813-ib",
    "be3814-ib", "be3815-ib", "be3816-ib", "be3817-ib", "be3818-ib", "be3819-ib",
    "be3820-ib", "be3821-ib"]
    nodes=bparse._get_nodes_in_stringIO(s)
    assert nodes == expected

def test_count_bad_items():
    list_of_lists = [["A", "B", "C"], ["B", "C", "D"]]
    expected = {"A": 1, "B": 2, "C": 2, "D": 1 }
    actual = bparse.count_bad_items(list_of_lists)
    assert actual == expected

def test_remove_good_items():
    potential_bad_list = {"A": 1, "B": 2, "C": 2, "D": 1 }
    list_of_lists = [["B","F"],["D","E"]]
    expected = {"A": 1, "C": 2}
    actual = bparse.remove_good_items(potential_bad_list, list_of_lists)
    assert actual == expected
