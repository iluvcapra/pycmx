from unittest import TestCase

import pycmx

class TestParse(TestCase):

    def test_edls(self):
        files = ["INS4_R1_010417.edl" ,
                  "STP R1 v082517.edl",
                  "ToD_R4_LOCK3.1_030618_Video.edl"
                ]
        
        counts = [ 287, 250 , 376 ]


        for fn, count in zip(files, counts):
            events = pycmx.parse_cmx3600("tests/edls/" + fn )
            self.assertTrue( len(events) == count )


