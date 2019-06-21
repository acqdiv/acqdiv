import io
import unittest

from acqdiv.parsers.turkish.TurkishCleaner import TurkishCleaner
from acqdiv.parsers.turkish.TurkishParser import TurkishParser
from acqdiv.parsers.turkish.TurkishReader import TurkishReader


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