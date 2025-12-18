from unittest import TestCase

from pycmx import parse_cmx3600


class Issue19Test(TestCase):
    def setUp(self):
        self.f = open("tests/edls/ISSUE_19_unusual01.edl")

    def test_parse(self):
        edl = parse_cmx3600(self.f, tolerant=True)
        for event in edl.events:
            self.assertIsNotNone(event.edits)
            if event.number == 1:
                self.assertEqual(len(event.edits), 1)
                self.assertEqual(event.edits[0].source, "Z125C001_220217_ROLX")
                self.assertEqual(event.edits[0].channels.v, True)
                self.assertEqual(event.edits[0].transition.kind, "C")
                self.assertEqual(event.edits[0].transition.operand, "")
                self.assertEqual(event.edits[0].source_in, "15:51:58:10")
                self.assertEqual(event.edits[0].record_out, "00:00:04:06")
                break

    def tearDown(self):
        self.f.close()
