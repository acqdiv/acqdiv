import io
import unittest
from acqdiv.parsers.chat.CHATParser import *
from acqdiv.parsers.chat.readers.ACQDIVCHATReader import ACQDIVCHATReader
from acqdiv.parsers.chat.cleaners.CHATCleaner import *


class TestCHATParser(unittest.TestCase):
    """Class to test the CHATParser."""

    def setUp(self):
        self.parser = CHATParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (CHATParser)"""
        actual_reader = CHATParser.get_reader()
        self.assertTrue(isinstance(actual_reader, ACQDIVCHATReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (CHATParser)"""
        actual_cleaner = CHATParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, CHATCleaner))

    def test_get_session_metadata(self):
        """Test get_session_metadata with TestCHATParser.cha. (CHATParser)"""
        session = (
            '@UTF8\n'
            '@Begin\n'
            '@Date:\t12-SEP-1997\n'
            '@Participants:\tMEM Mme_Manyili Grandmother , '
            'CHI Hlobohang Target_Child\n'
            '@ID:\tsme|Sesotho|MEM||female|||Grandmother|||\n'
            '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||\n'
            '@Birth of CHI:\t14-JAN-2006\n'
            '@Birth of MEM:\t11-OCT-1974\n'
            '@Media:\th2ab, audio\n'
            '@End'
        )
        self.parser.reader.read(io.StringIO(session))

        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'date': '1997-09-12',
            'media_filename': 'h2ab'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        """Test next_speaker with test.cha. (CHATParser)"""
        session = (
            '@UTF8\n'
            '@Begin\n'
            '@Date:\t12-SEP-1997\n'
            '@Participants:\tMEM Mme_Manyili Grandmother , '
            'CHI Hlobohang Target_Child\n'
            '@ID:\tsme|Sesotho|MEM||female|||Grandmother|||\n'
            '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||\n'
            '@Birth of CHI:\t14-JAN-2006\n'
            '@Birth of MEM:\t11-OCT-1974\n'
            '@Media:\th2ab, audio\n'
            '@End'
        )
        self.parser.reader.read(io.StringIO(session))

        actual_output = list(self.parser.next_speaker())
        mem_dict = {
            'speaker_label': 'MEM',
            'name': 'Mme_Manyili',
            'age_raw': None,
            'gender_raw': 'female',
            'role_raw': 'Grandmother',
            'languages_spoken': 'sme',
            'birthdate': '1974-10-11'
        }
        chi_dict = {
            'speaker_label': 'CHI',
            'name': 'Hlobohang',
            'age_raw': '2;2.',
            'gender_raw': None,
            'role_raw': 'Target_Child',
            'languages_spoken': 'sme',
            'birthdate': '2006-01-14'
        }
        desired_output = [mem_dict, chi_dict]
        self.assertEqual(actual_output, desired_output)

    def test_get_words_dict_simple_case(self):
        actual_utt = 'shoulda tested'
        target_utt = 'should_have tested'
        actual_output = self.parser.get_words_dict(actual_utt, target_utt)
        desired_output = [{
            'word_language': None,
            'word': 'shoulda',
            'word_actual': 'shoulda',
            'word_target': 'should_have',
            'warning': None
            },
            {
                'word_language': None,
                'word': 'tested',
                'word_actual': 'tested',
                'word_target': 'tested',
                'warning': None
            }
        ]
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
