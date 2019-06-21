import io
import unittest

from acqdiv.parsers.yucatec.YucatecCleaner import YucatecCleaner
from acqdiv.parsers.yucatec.YucatecParser import YucatecParser
from acqdiv.parsers.yucatec.YucatecReader import YucatecReader


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