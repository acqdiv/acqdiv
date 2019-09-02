import unittest
import io

from acqdiv.parsers.corpora.main.nungon.cleaner import NungonCleaner
from acqdiv.parsers.corpora.main.nungon.session_parser import NungonSessionParser
from acqdiv.parsers.corpora.main.nungon.reader import NungonReader


class TestNungonParser(unittest.TestCase):

    def setUp(self):
        self.parser = NungonSessionParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Nungon)"""
        actual_reader = NungonSessionParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, NungonReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Nungon)"""
        actual_cleaner = NungonSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, NungonCleaner))