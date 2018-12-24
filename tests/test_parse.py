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
            actual = len(list(edl.events ))
            self.assertTrue( actual == count , f"expected {count} in file {fn} but found {actual}")


    def test_events(self):
        edl = pycmx.parse_cmx3600("tests/edls/TEST.edl")
        events = list( edl.events  )
    
        self.assertEqual( int(events[0].number) , 1)
        self.assertEqual( events[0].edits[0].source , "OY_HEAD_")
        self.assertEqual( events[0].edits[0].clip_name , "HEAD LEADER MONO")
        self.assertEqual( events[0].edits[0].source_file , "OY_HEAD_LEADER.MOV")
        self.assertEqual( events[0].edits[0].source_in , "00:00:00:00")
        self.assertEqual( events[0].edits[0].source_out , "00:00:00:00")
        self.assertEqual( events[0].edits[0].record_in , "01:00:00:00")
        self.assertEqual( events[0].edits[0].record_out , "01:00:08:00")
        self.assertTrue( events[0].edits[0].transition.kind == pycmx.Transition.Cut)


    def test_multi_edit_events(self):
        edl = pycmx.parse_cmx3600("tests/edls/TEST.edl")
        events = list( edl.events  )


        self.assertEqual( int(events[42].number) , 43)
        self.assertEqual( len(events[42].edits), 2)

        
        self.assertEqual( events[42].edits[0].source , "TC_R1_V1")
        self.assertEqual( events[42].edits[0].clip_name , "TC R1 V1.2 TEMP1 FX ST.WAV")
        self.assertEqual( events[42].edits[0].source_in , "00:00:00:00")
        self.assertEqual( events[42].edits[0].source_out , "00:00:00:00")
        self.assertEqual( events[42].edits[0].record_in , "01:08:56:09")
        self.assertEqual( events[42].edits[0].record_out , "01:08:56:09")
        self.assertTrue( events[42].edits[0].transition.kind == pycmx.Transition.Cut)


        self.assertEqual( events[42].edits[1].source , "TC_R1_V6")
        self.assertEqual( events[42].edits[1].clip_name , "TC R1 V6 TEMP2 ST FX.WAV")
        self.assertEqual( events[42].edits[1].source_in , "00:00:00:00")
        self.assertEqual( events[42].edits[1].source_out , "00:00:00:00")
        self.assertEqual( events[42].edits[1].record_in , "01:08:56:09")
        self.assertEqual( events[42].edits[1].record_out , "01:08:56:11")
        self.assertTrue( events[42].edits[1].transition.kind == pycmx.Transition.Dissolve)



