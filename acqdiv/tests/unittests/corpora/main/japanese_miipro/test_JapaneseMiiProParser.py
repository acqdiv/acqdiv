import io
import unittest

from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProParser import \
    JapaneseMiiProParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader


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