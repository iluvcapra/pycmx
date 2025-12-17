from unittest import TestCase 

from pycmx import parse_cmx3600

class Issue19Test(TestCase):
    def setUp(self):
        self.f = open("tests/edls/ISSUE_19_unusual01.edl")

    
    def test_parse(self):
        edl = parse_cmx3600(self.f)
        for event in edl.events:
            self.assertIsNotNone(event.edits)
            if event.number == 1:
                self.assertEqual(len(event.edits), 1)
        

    def tearDown(self):
        self.f.close()
