from unittest import TestCase

import pycmx

class TestParse(TestCase):

    def test_edls(self):
        files = ["INS4_R1_010417.edl" ,
                  "STP R1 v082517.edl",
                  "ToD_R4_LOCK3.1_030618_Video.edl",
                  "TEST.edl"
                ]
        
        counts = [ 287, 250 , 376, 148  ]


        for fn, count in zip(files, counts):
            events = pycmx.parse_cmx3600(f"tests/edls/{fn}" )
            self.assertTrue( len(events) == count , f"expected {len(events)} but found {count}")

    def test_audio_channels(self):
        events = pycmx.parse_cmx3600(f"tests/edls/TEST.edl" )
        self.assertTrue(events[0].channels.a2)
        self.assertFalse(events[0].channels.a1)
        self.assertTrue(events[2].channels.get_audio_channel(7))


