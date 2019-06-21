import unittest

from acqdiv.parsers.corpora.main.nungon.NungonCleaner import NungonCleaner
from acqdiv.parsers.corpora.main.nungon.NungonParser import NungonParser
from acqdiv.parsers.corpora.main.nungon.NungonReader import NungonReader


class TestNungonParser(unittest.TestCase):

    def setUp(self):
        self.parser = NungonParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Nungon)"""
        actual_reader = NungonParser.get_reader()
        self.assertTrue(isinstance(actual_reader, NungonReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Nungon)"""
        actual_cleaner = NungonParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, NungonCleaner))