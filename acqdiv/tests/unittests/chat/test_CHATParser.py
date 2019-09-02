import acqdiv
import unittest
import io
from acqdiv.parsers.chat.parser import *
from acqdiv.parsers.chat.readers.reader import CHATReader
from acqdiv.parsers.chat.cleaners.cleaner import *


class TestCHATParser(unittest.TestCase):
    """Class to test the CHATParser."""

    def setUp(self):
        self.maxDiff = None
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

    def test_get_reader(self):
        """Test get_reader. (CHATParser)"""
        actual_reader = CHATParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, CHATReader))

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
        parser = CHATParser(self.dummy_cha_path)
        parser.reader = CHATReader(io.StringIO(session))

        session = parser.parse()
        oracle = (session.source_id == 'dummy'
                  and session.date == '1997-09-12'
                  and session.media_filename == 'h2ab')

        assert oracle

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
        parser = CHATParser(self.dummy_cha_path)
        parser.reader = CHATReader(io.StringIO(session))

        session = parser.parse()
        speaker_mem = session.speakers[0]
        speaker_chi = session.speakers[1]

        actual_mem_dict = {
            'speaker_label': speaker_mem.code,
            'name': speaker_mem.name,
            'age_raw': speaker_mem.age_raw,
            'gender_raw': speaker_mem.gender_raw,
            'role_raw': speaker_mem.role_raw,
            'languages_spoken': speaker_mem.languages_spoken,
            'birthdate': speaker_mem.birth_date
        }

        actual_chi_dict = {
            'speaker_label': speaker_chi.code,
            'name': speaker_chi.name,
            'age_raw': speaker_chi.age_raw,
            'gender_raw': speaker_chi.gender_raw,
            'role_raw': speaker_chi.role_raw,
            'languages_spoken': speaker_chi.languages_spoken,
            'birthdate': speaker_chi.birth_date
        }

        mem_dict = {
            'speaker_label': 'MEM',
            'name': 'Mme_Manyili',
            'age_raw': '',
            'gender_raw': 'female',
            'role_raw': 'Grandmother',
            'languages_spoken': 'sme',
            'birthdate': '1974-10-11'
        }
        chi_dict = {
            'speaker_label': 'CHI',
            'name': 'Hlobohang',
            'age_raw': '2;2.',
            'gender_raw': '',
            'role_raw': 'Target_Child',
            'languages_spoken': 'sme',
            'birthdate': '2006-01-14'
        }
        actual_output = [actual_mem_dict, actual_chi_dict]
        desired_output = [mem_dict, chi_dict]
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
