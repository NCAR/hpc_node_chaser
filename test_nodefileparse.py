import nodefile_parse
import cStringIO

def test_parse():
    s=cStringIO.StringIO("""
   r1i0n4,  r1i0n12,   r1i0n6,  r1i1n20,  r1i5n22,   r2i3n8,  r2i3n13,  r2i3n14,
  r4i0n16,  r4i1n30,  r4i1n23,  r4i1n24,  r4i1n25,  r4i1n26,  r4i1n31,  r4i1n32,
  r4i1n33,  r4i1n34,  r4i1n35,   r4i2n0
    """)

    expected = [["r1i0n4", "r1i0n12", "r1i0n6", "r1i1n20", "r1i5n22", "r2i3n8", "r2i3n13", "r2i3n14",
                 "r4i0n16", "r4i1n30", "r4i1n23", "r4i1n24", "r4i1n25", "r4i1n26", "r4i1n31", 
                 "r4i1n32", "r4i1n33", "r4i1n34", "r4i1n35", "r4i2n0"]]

    actual = nodefile_parse.parse(s)

    assert actual == expected
