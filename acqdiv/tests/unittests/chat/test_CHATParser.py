import io
import unittest
from acqdiv.parsers.chat.BaseCHATParser import *
from acqdiv.parsers.chat.readers.BaseCHATReader import BaseCHATReader
from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import *


class TestCHATParser(unittest.TestCase):
    """Class to test the BaseCHATParser."""

    def setUp(self):
        self.parser = BaseCHATParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (BaseCHATParser)"""
        actual_reader = BaseCHATParser.get_reader()
        self.assertTrue(isinstance(actual_reader, BaseCHATReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (BaseCHATParser)"""
        actual_cleaner = BaseCHATParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, BaseCHATCleaner))

    def test_get_session_metadata(self):
        """Test get_session_metadata with TestCHATParser.cha. (BaseCHATParser)"""
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
        """Test next_speaker with test.cha. (BaseCHATParser)"""
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
