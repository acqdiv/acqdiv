import io
import unittest

from acqdiv.parsers.corpora.main.english.reader import \
    EnglishManchester1Reader


class TestEnglishManchester1ReaderSpeaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Participants:\tMOT Mother , CHI Anna Target_Child\n'
                   '@ID:\teng|Manchester|MOT||female|||Mother|||\n'
                   '@ID:\teng|Manchester|CHI|1;10.07||||Target_Child|||\n'
                   '@End')
        cls.reader = EnglishManchester1Reader(io.StringIO(session))
        cls.reader.load_next_speaker()

    def test_get_speaker_name(self):
        """Test get_speaker_name."""
        actual_output = self.reader.get_speaker_name()
        desired_output = 'Mother of Anna'
        self.assertEqual(actual_output, desired_output)