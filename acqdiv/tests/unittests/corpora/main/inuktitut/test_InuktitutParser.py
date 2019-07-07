import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.inuktitut.InuktitutCleaner import \
    InuktitutCleaner
from acqdiv.parsers.corpora.main.inuktitut.InuktitutSessionParser import \
    InuktitutSessionParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutReader import \
    InuktitutReader


class TestInuktitutParser(unittest.TestCase):
    """
    Class to test InuktitutSessionParser.
    """

    def setUp(self):
        self.maxDiff = None
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

    def test_get_reader(self):
        """Test get_reader for Inuktitutparser."""
        actual_reader = InuktitutSessionParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, InuktitutReader))

    def test_get_cleaner(self):
        """Test get_cleaner for Inuktitutparser."""
        actual_cleaner = InuktitutSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, InuktitutCleaner))

    def test_next_utterance_no_misalignments_one_word(self):
        """Test next_utterance with one word and one morpheme. (Inuktitut)"""
        session_str = (
            '*MAE:\tAllaigutama  .\n%eng:\tGive me a comb  .\n%xmor:\tNR|'
            'ollaoguto^comb+NI|mim^MOD_SG .\n%tim:\t00:01:32\n%add:\tRO\n@End'
        )
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        actual_output = list(parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'dummy_0',
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
