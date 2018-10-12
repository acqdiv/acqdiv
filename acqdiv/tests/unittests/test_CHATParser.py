import io
import unittest
from acqdiv.parsers.chat.CHATParser import *
from acqdiv.parsers.chat.readers.ACQDIVCHATReader import ACQDIVCHATReader
from acqdiv.parsers.chat.CHATCleaner import *
from acqdiv.parsers.chat.readers.CreeReader import CreeReader
from acqdiv.parsers.chat.readers.InuktitutReader import InuktitutReader
from acqdiv.parsers.chat.readers.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.chat.readers.NungonReader import NungonReader
from acqdiv.parsers.chat.readers.SesothoReader import SesothoReader
from acqdiv.parsers.chat.readers.TurkishReader import TurkishReader
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
        with open('TestCHATParser.cha', 'r', encoding='utf8') as session:
            self.parser.reader.read(session)
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'date': '1997-09-12',
            'media_filename': 'h2ab'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        """Test next_speaker with test.cha. (CHATParser)"""
        with open('TestCHATParser.cha', 'r', encoding='utf8') as session:
            self.parser.reader.read(session)
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

###############################################################################


class TestInuktitutParser(unittest.TestCase):
    """
    Class to test InuktitutParser.
    """

    def setUp(self):
        self.parser = InuktitutParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader for Inuktitutparser."""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, InuktitutReader))

    def test_get_cleaner(self):
        """Test get_cleaner for Inuktitutparser."""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, InuktitutCleaner))

    def test_next_utterance_no_misalignments_one_word(self):
        """Test next_utterance with one word and one morpheme. (Inuktitut)"""
        session_str = (
            '*MAE:\tAllaigutama  .\n%eng:\tGive me a comb  .\n%xmor:\tNR|'
            'ollaoguto^comb+NI|mim^MOD_SG .\n%tim:\t00:01:32\n%add:\tRO\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MAE',
            'addressee': 'RO',
            'utterance_raw': 'Allaigutama  .',
            'utterance': 'Allaigutama',
            'translation': 'Give me a comb  .',
            'morpheme': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'gloss_raw': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'pos_raw': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'sentence_type': 'default',
            'start_raw': '00:01:32',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [{
            'word_language': None,
            'word': 'Allaigutama',
            'word_actual': 'Allaigutama',
            'word_target': 'Allaigutama',
            'warning': None
        }]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ollaoguto',
                    'gloss_raw': 'comb',
                    'pos_raw': 'NR'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'mim',
                    'gloss_raw': 'MOD_SG',
                    'pos_raw': 'NI'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with two words and morphemes. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with less words than morphemes. (Inuktitut)"""
        session_str = (
            '*AUN:\tana  ?\n%eng:\tit hurts there ?\n%xmor:\t'
            'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana  ?',
            'utterance': 'ana',
            'translation': 'it hurts there ?',
            'morpheme': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance, fewer segments than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_gloss_misaligned(self):
        """Test next_utterance, fewer glosses than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'gloss_raw': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'pos_raw': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance, fewer poses than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestJapaneseMiiProParser(unittest.TestCase):
    """Class to test the JapaneseMiiProParser."""

    def setUp(self):
        self.parser = JapaneseMiiProParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader for JapaneseMiiProParser."""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, JapaneseMiiProReader))

    def test_get_cleaner(self):
        """Test get_cleaner for JapaneseMiiProParser."""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, JapaneseMiiProCleaner))

    def test_next_utterance_no_misalignments_single_word(self):
        """Test next_utterance with no misalignemnts. (JapaneseMiiPro)"""
        session_str = ('*MOT:\tnani ? 107252_107995\n%xtrn:\tn:deic:wh|nani'
                       ' ?\n%ort:\t何 ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'nani ?',
            'utterance': 'nani',
            'translation': None,
            'morpheme': 'n:deic:wh|nani ?',
            'gloss_raw': 'n:deic:wh|nani ?',
            'pos_raw': 'n:deic:wh|nani ?',
            'sentence_type': 'question',
            'start_raw': '107252',
            'end_raw': '107995',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'nani',
                'word_actual': 'nani',
                'word_target': 'nani',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'nani',
                    'morpheme_language': None,
                    'pos_raw': 'n:deic:wh'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with no misalignemnts. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g|doozo .',
            'gloss_raw': 'n:prop|Hono-chan co:g|doozo .',
            'pos_raw': 'n:prop|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with too few words. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tdoozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'doozo .',
            'utterance': 'doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g|doozo .',
            'gloss_raw': 'n:prop|Hono-chan co:g|doozo .',
            'pos_raw': 'n:prop|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance with too few segments. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g| .',
            'gloss_raw': 'n:prop|Hono-chan co:g| .',
            'pos_raw': 'n:prop|Hono-chan co:g| .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance with too few poses. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\t|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': '|Hono-chan co:g|doozo .',
            'gloss_raw': '|Hono-chan co:g|doozo .',
            'pos_raw': '|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': None
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestCreeParser(unittest.TestCase):
    """Class to test the CreeParser."""

    def setUp(self):
        self.parser = CreeParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Cree)"""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, CreeReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Cree)"""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, CreeCleaner))

    def test_next_utterance_no_misalignments_single_word(self):
        """Test next_utterance with utt containing no misalignemnts. (Cree)"""
        session_str = ('*CHI:\tchair . 2883660_2884622\n%pho:\t*\n%mod:\t*\n'
                       '%eng:\tohhhhhh\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': 'chair .',
            'utterance': 'chair',
            'translation': 'ohhhhhh',
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'default',
            'start_raw': '2883660',
            'end_raw': '2884622',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'chair',
                'word_actual': 'chair',
                'word_target': 'chair',
                'warning': None
            }
        ]
        morpheme_list = []
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with utt containing no misalignemnts. (Cree)"""

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu nîyi› .',
            'utterance': 'wâu nîyi',
            'translation': 'egg me',
            'morpheme': '[wo *]',
            'gloss_raw': '[egg 1]',
            'pos_raw': '[ni pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nîyi',
                'word_actual': 'nîyi',
                'word_target': 'nîyi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'egg',
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': 'ni'
                },
            ],
            [
                {
                    'gloss_raw': '1',
                    'morpheme': None,
                    'morpheme_language': 'Cree',
                    'pos_raw': 'pro'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with too few words. (Cree)"""

        session_str = ('*CHI:\t‹wâu› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu› .',
            'utterance': 'wâu',
            'translation': 'egg me',
            'morpheme': '[wo *]',
            'gloss_raw': '[egg 1]',
            'pos_raw': '[ni pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'egg',
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': 'ni'
                },
            ],
            [
                {
                    'gloss_raw': '1',
                    'morpheme': None,
                    'morpheme_language': 'Cree',
                    'pos_raw': 'pro'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance with too few segments. (Cree)

        In Cree the segment tier is the main morphology tier (not the
        gloss tier). This means that in the desired output, there are
        only as many morpheme words as there are segment words. The
        surplus words of the other tiers thus get removed.
        """

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu nîyi› .',
            'utterance': 'wâu nîyi',
            'translation': 'egg me',
            'morpheme': '[wo]',
            'gloss_raw': '[egg 1]',
            'pos_raw': '[ni pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nîyi',
                'word_actual': 'nîyi',
                'word_target': 'nîyi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': None
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_glosses_misaligned(self):
        """Test next_utterance with too few glosses. (Cree)

        In Cree the segment tier is the main morphology tier (not the
        gloss tier). This means that in the desired output, the number
        of morpheme words is not dependent on the glosses but on the
        segments. The desired output of this test case thus contains two
        morpheme words even though there is only one gloss word.
        """

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu nîyi› .',
            'utterance': 'wâu nîyi',
            'translation': 'egg me',
            'morpheme': '[wo *]',
            'gloss_raw': '[egg]',
            'pos_raw': '[ni pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nîyi',
                'word_actual': 'nîyi',
                'word_target': 'nîyi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': 'ni'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': None,
                    'morpheme_language': 'Cree',
                    'pos_raw': 'pro'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance with too few poses. (Cree)"""

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu nîyi› .',
            'utterance': 'wâu nîyi',
            'translation': 'egg me',
            'morpheme': '[wo *]',
            'gloss_raw': '[egg 1]',
            'pos_raw': '[pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nîyi',
                'word_actual': 'nîyi',
                'word_target': 'nîyi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'egg',
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': None
                },
            ],
            [
                {
                    'gloss_raw': '1',
                    'morpheme': None,
                    'morpheme_language': 'Cree',
                    'pos_raw': None
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


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
        session_str = ('*HLE:\t Tsebo . 1870096_1871196\n%gls:\tTsebo .\n'
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
            'utterance_raw': 'e tsamaya (uye) (ho)dula pela ausi Mamello .',
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
            'utterance_raw': 'tsamaya .',
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
            'utterance_raw': 'e tsamaya .',
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


class TestTurkishParser(unittest.TestCase):

    def setUp(self):
        self.parser = TurkishParser('__init__.py')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Sesotho)"""
        actual_reader = TurkishParser.get_reader()
        self.assertTrue(isinstance(actual_reader, TurkishReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Sesotho)"""
        actual_cleaner = TurkishParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, TurkishCleaner))

    def test_next_utterance_no_misalignments_single_word_no_mor(self):
        """Test next_utterance with utt containing no misalignemnts. (Turkish)

        Test with a one-word utterance without morphology.
        """
        session_str = '*GRA:\tne ?\n%add:\tMOT\n@End'
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'GRA',
            'addressee': 'MOT',
            'utterance_raw': 'ne ?',
            'utterance': 'ne',
            'translation': None,
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'ne',
                'word_actual': 'ne',
                'word_target': 'ne',
                'warning': None
            }
        ]
        morpheme_list = []
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words_with_mor(self):
        """Test next_utterance with utt containing 2 words. (Turkish)

        Utterance contains morphology.
        """
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE V|iste-IPFV-2S ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi istiyo(r)sun ?',
            'utterance': 'inmekmi istiyosun',
            'translation': None,
            'morpheme': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'gloss_raw': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'pos_raw': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            },
            {
                'word_language': 'Turkish',
                'word': 'istiyosun',
                'word_actual': 'istiyosun',
                'word_target': 'istiyorsun',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'iste',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'IPFV',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': '2S',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'}
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with too few words. (Turkish)"""
        session_str = ('*BAB:\tinmekmi ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE V|iste-IPFV-2S ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi ?',
            'utterance': 'inmekmi',
            'translation': None,
            'morpheme': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'gloss_raw': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'pos_raw': 'V|in-INF-QUE V|iste-IPFV-2S ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'iste',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'IPFV',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': '2S',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_morphology_misaligned(self):
        """Test next_utterance with too few morpheme words. (Turkish)

        Misalignment on the morpheme tier (xmor) which includes glosses,
        poses and segments.
        """
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi istiyo(r)sun ?',
            'utterance': 'inmekmi istiyosun',
            'translation': None,
            'morpheme': 'V|in-INF-QUE ?',
            'gloss_raw': 'V|in-INF-QUE ?',
            'pos_raw': 'V|in-INF-QUE ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            },
            {
                'word_language': 'Turkish',
                'word': 'istiyosun',
                'word_actual': 'istiyosun',
                'word_target': 'istiyorsun',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance with too few poses. (Turkish)"""
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE |iste-IPFV-2S ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi istiyo(r)sun ?',
            'utterance': 'inmekmi istiyosun',
            'translation': None,
            'morpheme': 'V|in-INF-QUE |iste-IPFV-2S ?',
            'gloss_raw': 'V|in-INF-QUE |iste-IPFV-2S ?',
            'pos_raw': 'V|in-INF-QUE |iste-IPFV-2S ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            },
            {
                'word_language': 'Turkish',
                'word': 'istiyosun',
                'word_actual': 'istiyosun',
                'word_target': 'istiyorsun',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'iste',
                    'morpheme_language': None,
                    'pos_raw': None
                }, {
                    'gloss_raw': 'IPFV',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': '2S',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'}
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance with too few segments. (Turkish)"""
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE V|-IPFV-2S ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi istiyo(r)sun ?',
            'utterance': 'inmekmi istiyosun',
            'translation': None,
            'morpheme': 'V|in-INF-QUE V|-IPFV-2S ?',
            'gloss_raw': 'V|in-INF-QUE V|-IPFV-2S ?',
            'pos_raw': 'V|in-INF-QUE V|-IPFV-2S ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            },
            {
                'word_language': 'Turkish',
                'word': 'istiyosun',
                'word_actual': 'istiyosun',
                'word_target': 'istiyorsun',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'IPFV',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': '2S',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'}
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_glosses_misaligned(self):
        """Test next_utterance with too few glosses. (Turkish)"""
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n%add:\tCHI\n%xmor:\t'
                       'V|in-INF-QUE V|iste ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': '__init___0',
            'speaker_label': 'BAB',
            'addressee': 'CHI',
            'utterance_raw': 'inmekmi istiyo(r)sun ?',
            'utterance': 'inmekmi istiyosun',
            'translation': None,
            'morpheme': 'V|in-INF-QUE V|iste ?',
            'gloss_raw': 'V|in-INF-QUE V|iste ?',
            'pos_raw': 'V|in-INF-QUE V|iste ?',
            'sentence_type': 'question',
            'start_raw': None,
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Turkish',
                'word': 'inmekmi',
                'word_actual': 'inmekmi',
                'word_target': 'inmekmi',
                'warning': None
            },
            {
                'word_language': 'Turkish',
                'word': 'istiyosun',
                'word_actual': 'istiyosun',
                'word_target': 'istiyorsun',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'in',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }, {
                    'gloss_raw': 'INF',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }, {
                    'gloss_raw': 'QUE',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                }
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'iste',
                    'morpheme_language': None,
                    'pos_raw': 'V'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

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
            'translation': None,
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
