import io
import unittest

from acqdiv.parsers.corpora.main.nungon.reader import NungonReader


class TestNungonReaderRecord(unittest.TestCase):
    """Test record readers of NungonReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '*MEM:\t&foo ma(i)nline [: utterance]. \x150_1111\x15\n'
                   '%xgls:\tThis is the segment tier\n'
                   '%xcod:\tThis is the gloss/POS tier\n'
                   '@End')
        cls.reader = NungonReader(io.StringIO(session))
        cls.reader.load_next_record()

    def test_get_seg_tier(self):
        actual_output = self.reader.get_seg_tier()
        desired_output = 'This is the segment tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier(self):
        actual_output = self.reader.get_gloss_tier()
        desired_output = 'This is the gloss/POS tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier(self):
        actual_output = self.reader.get_pos_tier()
        desired_output = 'This is the gloss/POS tier'
        self.assertEqual(actual_output, desired_output)