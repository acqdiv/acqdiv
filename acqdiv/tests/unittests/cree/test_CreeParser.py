import io
import unittest

from acqdiv.parsers.cree.CreeCleaner import CreeCleaner
from acqdiv.parsers.cree.CreeParser import CreeParser
from acqdiv.parsers.cree.CreeReader import CreeReader


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