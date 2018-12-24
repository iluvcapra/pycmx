from unittest import TestCase

import pycmx

class TestParse(TestCase):

    def test_edls(self):
        files = ["INS4_R1_010417.edl" ,
                  "STP R1 v082517.edl",
                  "ToD_R4_LOCK3.1_030618_Video.edl",
                  "TEST.edl"
                ]
        
        counts = [ 287, 250 , 376, 120  ]


        for fn, count in zip(files, counts):
            edl = pycmx.parse_cmx3600(f"tests/edls/{fn}" )
            actual = len(edl.events())
            self.assertTrue( actual == count , f"expected {count} but found {actual}")



