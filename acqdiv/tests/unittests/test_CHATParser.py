import io
import unittest
from acqdiv.parsers.chat.CHATParser import *
from acqdiv.parsers.chat.cleaners.NungonCleaner import NungonCleaner
from acqdiv.parsers.chat.cleaners.SesothoCleaner import SesothoCleaner
from acqdiv.parsers.chat.cleaners.YucatecCleaner import YucatecCleaner
from acqdiv.parsers.chat.readers.ACQDIVCHATReader import ACQDIVCHATReader
from acqdiv.parsers.chat.cleaners.CHATCleaner import *
from acqdiv.parsers.chat.readers.NungonReader import NungonReader
from acqdiv.parsers.chat.readers.SesothoReader import SesothoReader
from acqdiv.parsers.chat.readers.YucatecReader import YucatecReader


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


class TestSesothoParser(unittest.TestCase):
    """Class to test the SesothoParser.

    There are no tests for misalignments between words and the morpheme
    tiers since the words are replaced by morphemes anyway.

    There are no tests for misaligned poses either, because they are
    encoded (and thus also tested) in the gloss_tier.
    """

    def setUp(self):
        self.parser = SesothoParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Sesotho)"""
        actual_reader = SesothoParser.get_reader()
        self.assertTrue(isinstance(actual_reader, SesothoReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Sesotho)"""
        actual_cleaner = SesothoParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, SesothoCleaner))

    def test_next_utterance_no_misalignments_single_word(self):
        """Test next_utterance with utt containing no misalignemnts. (Sesotho)

        Test with a one-word utterance.
        """
        session_str = ('*HLE:\tTsebo . 1870096_1871196\n%gls:\tTsebo .\n'
                       '%cod:\tn^name .\n%eng:\tTsebo !\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'HLE',
            'addressee': None,
            'utterance_raw': 'Tsebo .',
            'utterance': 'Tsebo',
            'translation': 'Tsebo !',
            'morpheme': 'Tsebo .',
            'gloss_raw': 'n^name .',
            'pos_raw': 'n^name .',
            'sentence_type': 'default',
            'start_raw': '1870096',
            'end_raw': '1871196',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'Tsebo',
                'word_actual': 'Tsebo',
                'word_target': 'Tsebo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'a_name',
                    'morpheme': 'Tsebo',
                    'morpheme_language': None,
                    'pos_raw': '???'
                },
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with utt containing no misalignments. (Sesotho)

        Utterance contains contraction parentheses and infinitive
        parentheses.
        """

        session_str = ('*MHL:\te tsamo dula pela ausi Mamello . 113200_115376'
                       '\n%gls:\te tsamay-a (u-y-e) (ho-)dul-a pela ausi '
                       'Mamello .\n%cod:\tij v^leave-m^i (sm2s-t^p_v^go-m^s) '
                       '(if-)v^sit-m^in loc sister(1a , 2a) n^name .\n%eng:\t'
                       'Yes go and (go) sit next to sister Mamello\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MHL',
            'addressee': None,
            'utterance_raw': 'e tsamo dula pela ausi Mamello .',
            'utterance': 'e tsamaya hodula pela ausi Mamello',
            'translation': 'Yes go and (go) sit next to sister Mamello',
            'morpheme': 'e tsamay-a (u-y-e) (ho-)dul-a pela ausi Mamello .',
            'gloss_raw': ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in '
                          'loc sister(1a , 2a) n^name .'),
            'pos_raw': ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in '
                        'loc sister(1a , 2a) n^name .'),
            'sentence_type': 'default',
            'start_raw': '113200',
            'end_raw': '115376',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'e',
                'word_actual': 'e',
                'word_target': 'e',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'tsamaya',
                'word_actual': 'tsamaya',
                'word_target': 'tsamaya',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'hodula',
                'word_actual': 'hodula',
                'word_target': 'hodula',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'pela',
                'word_actual': 'pela',
                'word_target': 'pela',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'ausi',
                'word_actual': 'ausi',
                'word_target': 'ausi',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'Mamello',
                'word_actual': 'Mamello',
                'word_target': 'Mamello',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'ij',
                    'morpheme': 'e',
                    'morpheme_language': None,
                    'pos_raw': 'ij'
                }
            ],
            [
                {
                    'gloss_raw': 'leave',
                    'morpheme': 'tsamay',
                    'morpheme_language': None,
                    'pos_raw': 'v'
                },
                {
                    'gloss_raw': 'm^i',
                    'morpheme': 'a',
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': 'if',
                    'morpheme': 'ho',
                    'morpheme_language': None,
                    'pos_raw': 'pfx'
                },
                {
                    'gloss_raw': 'sit',
                    'morpheme': 'dul',
                    'morpheme_language': None,
                    'pos_raw': 'v'
                },
                {
                    'gloss_raw': 'm^in',
                    'morpheme': 'a',
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': 'loc',
                    'morpheme': 'pela',
                    'morpheme_language': None,
                    'pos_raw': 'loc'
                }
            ],
            [
                {
                    'gloss_raw': 'sister(1a,2a)',
                    'morpheme': 'ausi',
                    'morpheme_language': None,
                    'pos_raw': 'n'
                }
            ],
            [
                {
                    'gloss_raw': 'a_name',
                    'morpheme': 'Mamello',
                    'morpheme_language': None,
                    'pos_raw': '???'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_morphemes_misaligned(self):
        """Test next_utterance with too few morphemes. (Sesotho)"""

        session_str = ('*NHL:\te tsamo . 113200_115376\n%gls:\ttsamay-a '
                       '.\n%cod:\tij v^leave-m^i '
                       '.\n%eng:\tYes go and\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'NHL',
            'addressee': None,
            'utterance_raw': 'e tsamo .',
            'utterance': 'tsamaya',
            'translation': 'Yes go and',
            'morpheme': 'tsamay-a .',
            'gloss_raw': 'ij v^leave-m^i .',
            'pos_raw': 'ij v^leave-m^i .',
            'sentence_type': 'default',
            'start_raw': '113200',
            'end_raw': '115376',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'tsamaya',
                'word_actual': 'tsamaya',
                'word_target': 'tsamaya',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'ij',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'ij'
                }
            ],
            [
                {
                    'gloss_raw': 'leave',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'v'
                },
                {
                    'gloss_raw': 'm^i',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_glosses_misaligned(self):
        """Test next_utterance with too few glosses. (Sesotho)"""

        session_str = ('*NHM:\te tsamo . 113200_115376\n%gls:\te tsamay-a .'
                       '\n%cod:\tv^leave-m^i .\n%eng:\tYes go and\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'NHM',
            'addressee': None,
            'utterance_raw': 'e tsamo .',
            'utterance': 'e tsamaya',
            'translation': 'Yes go and',
            'morpheme': 'e tsamay-a .',
            'gloss_raw': 'v^leave-m^i .',
            'pos_raw': 'v^leave-m^i .',
            'sentence_type': 'default',
            'start_raw': '113200',
            'end_raw': '115376',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'e',
                'word_actual': 'e',
                'word_target': 'e',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'tsamaya',
                'word_actual': 'tsamaya',
                'word_target': 'tsamaya',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'leave',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'v'
                },
                {
                    'gloss_raw': 'm^i',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


###############################################################################


class TestYucatecParser(unittest.TestCase):

    def setUp(self):
        self.parser = YucatecParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Yucatec)"""
        actual_reader = YucatecParser.get_reader()
        self.assertTrue(isinstance(actual_reader, YucatecReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Yucatec)"""
        actual_cleaner = YucatecParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, YucatecCleaner))

    def test_next_utterance_no_misalignments_single_word_no_mor(self):
        """Test next_utterance with utt containing no misalignemnts. (Turkish)

        Test with a one-word utterance without morphology.
        """
        session_str = ('*LOR:\tbaʼax .\n%xpho:\tbaaʼx\n%xmor:\tINT|baʼax .\n'
                       '%xspn:\tqué .\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'LOR',
            'addressee': None,
            'utterance_raw': 'baʼax .',
            'utterance': 'baʼax',
            'translation': 'qué .',
            'morpheme': 'INT|baʼax .',
            'gloss_raw': 'INT|baʼax .',
            'pos_raw': 'INT|baʼax .',
            'sentence_type': 'default',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'baʼax',
                'word_actual': 'baʼax',
                'word_target': 'baʼax',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'baʼax',
                    'morpheme_language': None,
                    'pos_raw': 'INT'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


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


if __name__ == '__main__':
    unittest.main()
