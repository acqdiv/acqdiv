import unittest
from cleaning2.scripts.clean import Cleaner

class CleanerTestCase(unittest.TestCase):
    """ Tests for cleaner.py """
    
    def setUp(self):
        self.c = Cleaner("../../cleaning2/input/inuktitut/rules/inuktitut.conf")
