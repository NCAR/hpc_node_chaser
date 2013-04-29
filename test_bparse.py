import bparse
import cStringIO

def test_get_nodes_in_stringIO():
    s=cStringIO.StringIO("""
Sat Apr 20 03:48:51 2013: Dispatched to 16384 Hosts/Processors <16*ys3769-ib> <
                          16*ys3770-ib> <16*ys3771-ib> <16*ys3772-ib> <16*ys380
                          1-ib> <16*ys3802-ib> <16*ys3803-ib> <16*ys3804-ib> <1
                          6*ys3805-ib> <16*ys3806-ib> <16*ys3807-ib> <16*ys3808
                          -ib> <16*ys3809-ib> <16*ys3810-ib> <16*ys3811-ib> <16
                          *ys3812-ib> <16*ys3813-ib> <16*ys3814-ib> <16*ys3815-
                          ib> <16*ys3816-ib> <16*ys3817-ib> <16*ys3818-ib> <16*
                          ys3819-ib> <16*ys3820-ib> <16*ys3821-ib> 
    """)
    expected = ["ys3769-ib", "ys3770-ib", "ys3771-ib", "ys3772-ib", "ys3801-ib", 
    "ys3802-ib", "ys3803-ib", "ys3804-ib", "ys3805-ib", "ys3806-ib", "ys3807-ib", 
    "ys3808-ib", "ys3809-ib", "ys3810-ib", "ys3811-ib", "ys3812-ib", "ys3813-ib",
    "ys3814-ib", "ys3815-ib", "ys3816-ib", "ys3817-ib", "ys3818-ib", "ys3819-ib",
    "ys3820-ib", "ys3821-ib"]
    nodes=bparse._get_nodes_in_stringIO(s)
    assert nodes == expected
