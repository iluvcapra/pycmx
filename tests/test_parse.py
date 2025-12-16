from unittest import TestCase

import pycmx


class TestParse(TestCase):

    files = ["INS4_R1_010417.edl",
             "INS4_R1_DX_092117.edl",
             "STP R1 v082517.edl",
             "ToD_R4_LOCK3.1_030618_Video.edl",
             "TEST.edl",
             "test_edl_cdl.edl",
             "INS4_R1_DX_092117.edl"
             ]

    def test_event_counts(self):

        counts = [287, 466, 250, 376, 120, 3, 466]

        for fn, count in zip(type(self).files, counts):
            with open("tests/edls/" + fn, 'r') as f:
                edl = pycmx.parse_cmx3600(f)
                actual = len(list(edl.events))
                self.assertTrue(actual == count,
                                "expected %i in file %s but found %i"
                                % (count, fn, actual))

    def test_list_sanity(self):
        for fn in type(self).files:
            with open("tests/edls/" + fn, 'r') as f:
                edl = pycmx.parse_cmx3600(f)
                self.assertTrue(type(edl.title) is str)
                self.assertTrue(len(edl.title) > 0)

    def test_event_sanity(self):
        for fn in type(self).files:
            path = "tests/edls/" + fn
            with open(path, 'r') as f:
                edl = pycmx.parse_cmx3600(f)
                for index, event in enumerate(edl.events):
                    self.assertTrue(len(event.edits) > 0,
                                    f"Failed for {path}")
                    self.assertEqual(event.number, index + 1,
                                     f"Failed for {path}")

    def test_events(self):
        with open("tests/edls/TEST.edl", 'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list(edl.events)

            self.assertEqual(events[0].number, 1)
            self.assertEqual(events[0].edits[0].source, "OY_HEAD_")
            self.assertEqual(events[0].edits[0].clip_name, "HEAD LEADER MONO")
            self.assertEqual(
                events[0].edits[0].source_file, "OY_HEAD_LEADER.MOV")
            self.assertEqual(events[0].edits[0].source_in, "00:00:00:00")
            self.assertEqual(events[0].edits[0].source_out, "00:00:00:00")
            self.assertEqual(events[0].edits[0].record_in, "01:00:00:00")
            self.assertEqual(events[0].edits[0].record_out, "01:00:08:00")
            self.assertTrue(
                events[0].edits[0].transition.kind == pycmx.Transition.Cut)

    def test_channel_map(self):
        with open("tests/edls/TEST.edl", 'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list(edl.events)
            self.assertFalse(events[0].edits[0].channels.video)
            self.assertFalse(events[0].edits[0].channels.a1)
            self.assertTrue(events[0].edits[0].channels.a2)
            self.assertTrue(events[2].edits[0].channels.get_audio_channel(7))
            self.assertTrue(events[2].edits[0].channels.audio)

    def test_multi_edit_events(self):
        with open("tests/edls/TEST.edl", 'r') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list(edl.events)

            self.assertEqual(events[42].number, 43)
            self.assertEqual(len(events[42].edits), 2)

            self.assertEqual(events[42].edits[0].source, "TC_R1_V1")
            self.assertEqual(events[42].edits[0].clip_name,
                             "TC R1 V1.2 TEMP1 FX ST.WAV")
            self.assertEqual(events[42].edits[0].source_in, "00:00:00:00")
            self.assertEqual(events[42].edits[0].source_out, "00:00:00:00")
            self.assertEqual(events[42].edits[0].record_in, "01:08:56:09")
            self.assertEqual(events[42].edits[0].record_out, "01:08:56:09")
            self.assertTrue(
                events[42].edits[0].transition.kind == pycmx.Transition.Cut)

            self.assertEqual(events[42].edits[1].source, "TC_R1_V6")
            self.assertEqual(events[42].edits[1].clip_name,
                             "TC R1 V6 TEMP2 ST FX.WAV")
            self.assertEqual(events[42].edits[1].source_in, "00:00:00:00")
            self.assertEqual(events[42].edits[1].source_out, "00:00:00:00")
            self.assertEqual(events[42].edits[1].record_in, "01:08:56:09")
            self.assertEqual(events[42].edits[1].record_out, "01:08:56:11")
            self.assertTrue(
                events[42].edits[1].transition.kind ==
                pycmx.Transition.Dissolve)

    def test_line_numbers(self):
        with open("tests/edls/ToD_R4_LOCK3.1_030618_Video.edl") as f:
            edl = pycmx.parse_cmx3600(f)

            events = list(edl.events)
            self.assertEqual(events[0].edits[0].line_number, 2)
            self.assertEqual(events[14].edits[0].line_number, 45)
            self.assertEqual(events[180].edits[0].line_number, 544)

    def test_transition_name(self):
        with open("tests/edls/test_25.edl", "r") as f:
            edl = pycmx.parse_cmx3600(f)
            events = list(edl.events)
            self.assertEqual(
                events[4].edits[1].transition.name,  "CROSS DISSOLVE")

    def test_adobe_wide(self):
        with open("tests/edls/adobe_dai109_test.txt", 'r',
                  encoding='ISO-8859-1') as f:
            edl = pycmx.parse_cmx3600(f)
            events = list(edl.events)

            self.assertEqual(len(events), 2839)

    def test_issue14(self):
        with open("tests/edls/ISSUE_14_conform_edl_issue_03.edl", "r") as f:
            edl = pycmx.parse_cmx3600(f)

            for event in edl.events:
                if event.number == 42:
                    self.assertEqual(len(event.edits), 1)
                    self.assertEqual(event.edits[0].source,
                                     "M018C0005_240925_1F4L13")
                    self.assertEqual(event.edits[0].transition.kind,
                                     pycmx.Transition.Cut)
                    self.assertEqual(event.edits[0].source_in,
                                     "18:44:20:12")

    def test_cdl(self):
        with open("tests/edls/cdl_example01.edl", "r") as f:
            edl = pycmx.parse_cmx3600(f)
            for event in edl.events:
                if event.number == 1:
                    sop = event.edits[0].asc_sop_statement
                    self.assertIsNotNone(sop)
                    assert sop
                    self.assertEqual(sop.slope_r, "0.9405")
                    self.assertEqual(sop.offset_g, "-0.0276")

                    sat = event.edits[0].asc_sat_statement
                    self.assertIsNotNone(sat)
                    assert sat
                    self.assertEqual(sat.value, '0.9640')

    def test_frmc(self):
        with open("tests/edls/cdl_frmc_example01.edl", "r") as f:
            edl = pycmx.parse_cmx3600(f)
            for event in edl.events:
                if event.number == 1:
                    frmc = event.edits[0].frmc_statement
                    self.assertIsNotNone(frmc)
                    assert frmc
                    self.assertEqual(frmc.start, "1001")
                    self.assertEqual(frmc.end, "1102")
                    self.assertEqual(frmc.duration, "102")

        with open("tests/edls/cdl_frmc_example02.edl", "r") as f:
            edl = pycmx.parse_cmx3600(f)
            for event in edl.events:
                if event.number == 6:
                    frmc = event.edits[0].frmc_statement
                    self.assertIsNotNone(frmc)
                    assert frmc
                    self.assertEqual(frmc.start, "1001")
                    self.assertEqual(frmc.end, "1486")
                    self.assertEqual(frmc.duration, "486")
