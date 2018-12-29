from unittest import TestCase

import pycmx

class TestParse(TestCase):

    files = ["INS4_R1_010417.edl" ,
        "INS4_R1_DX_092117.edl",
          "STP R1 v082517.edl",
          "ToD_R4_LOCK3.1_030618_Video.edl",
          "TEST.edl",
          "test_edl_cdl.edl",
          "INS4_R1_DX_092117.edl"
        ]

    def test_event_counts(self):

        counts = [ 287, 466, 250 , 376, 120 , 3 , 466 ]

        for fn, count in zip(type(self).files, counts):
            with open(f"tests/edls/{fn}" ,'r') as f:
                edl = pycmx.parse_cmx3600(f)
                actual = len( list( edl.events ))
                self.assertTrue( actual == count , f"expected {count} in file {fn} but found {actual}")

    def test_list_sanity(self):
        for fn in type(self).files:
            with open(f"tests/edls/{fn}" ,'r') as f:
                edl = pycmx.parse_cmx3600(f)
                self.assertTrue( type(edl.title) is str )
                self.assertTrue( len(edl.title) > 0 )
    

    def test_event_sanity(self):
        for fn in type(self).files:
            with open(f"tests/edls/{fn}" ,'r') as f:
                edl = pycmx.parse_cmx3600(f)
                for index, event in enumerate(edl.events):
                    self.assertTrue( len(event.edits) > 0 )
                    self.assertTrue( event.number == index + 1 )



    def test_events(self):
        with open("tests/edls/TEST.edl",'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list( edl.events  )
        
            self.assertEqual( events[0].number , 1)
            self.assertEqual( events[0].edits[0].source , "OY_HEAD_")
            self.assertEqual( events[0].edits[0].clip_name , "HEAD LEADER MONO")
            self.assertEqual( events[0].edits[0].source_file , "OY_HEAD_LEADER.MOV")
            self.assertEqual( events[0].edits[0].source_in , "00:00:00:00")
            self.assertEqual( events[0].edits[0].source_out , "00:00:00:00")
            self.assertEqual( events[0].edits[0].record_in , "01:00:00:00")
            self.assertEqual( events[0].edits[0].record_out , "01:00:08:00")
            self.assertTrue( events[0].edits[0].transition.kind == pycmx.Transition.Cut)

    def test_channel_map(self):
        with open("tests/edls/TEST.edl",'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list( edl.events  )
            self.assertFalse( events[0].edits[0].channels.video)
            self.assertFalse( events[0].edits[0].channels.a1)
            self.assertTrue( events[0].edits[0].channels.a2)
            self.assertTrue( events[2].edits[0].channels.get_audio_channel(7) )


    def test_multi_edit_events(self):
        with open("tests/edls/TEST.edl",'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list( edl.events )

            self.assertEqual( events[42].number , 43)
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

    def test_line_numbers(self):
        with open("tests/edls/ToD_R4_LOCK3.1_030618_Video.edl") as f:
            edl = pycmx.parse_cmx3600(f)

            events = list( edl.events )
            self.assertEqual( events[0].edits[0].line_number, 2)
            self.assertEqual( events[14].edits[0].line_number, 45)
            self.assertEqual( events[180].edits[0].line_number, 544)


