import os
import unittest

import acqdiv
from acqdiv.parsers.corpora.main.russian.RussianSessionParser import \
    RussianSessionParser


class TestRussianParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        toolbox_path = os.path.join(
            here,
            'tests/unittests/corpora/main/russian/test_files/Russian.txt')

        metadata_path = os.path.join(
            here,
            'tests/unittests/corpora/main/russian/test_files/Russian.imdi')

        cls.parser = RussianSessionParser(toolbox_path, metadata_path)

    def test_get_session_metadata(self):
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'id': 'Russian',
            'date': 'session date',
            'genre': 'genre',
            'location': {},
            'situation': 'situation',
            'media_type': None
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        actual_output = next(self.parser.next_speaker())
        desired_output = {
            'role': 'actor role',
            'name': 'actor name',
            'fullname': 'actor fullname',
            'code': 'actor code',
            'familysocialrole': 'actor family social role',
            'languages': 'actor language id',
            'ethnicgroup': 'actor ethnic group',
            'age': 'actor age',
            'birthdate': 'actor birthdate',
            'sex': 'actor sex',
            'education': 'actor education'}
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance(self):
        actual_output = list(self.parser.next_utterance())

        utterance = {
            'source_id': 'source_id',
            'start_raw': 'start_raw',
            'end_raw': 'end_raw',
            'speaker_label': 'speaker_label',
            'addressee': None,
            'childdirected': None,
            'utterance_raw': 'w1 "," w2 w3 .',
            'utterance': 'w1 w2 w3',
            'sentence_type': 'default',
            'translation': None,
            'comment': None,
            'warning': None,
            'morpheme': 'lem1 "," lem2 lem3 .',
            'gloss_raw': 'PST:SG:F:IRREFL:IPFV NOM:SG PCL',
            'pos_raw': 'V-PST:SG:F:IRREFL:IPFV PUNCT PRO-DEM-NOUN:NOM:SG PCL '
                       'PUNCT'}

        words = [
            {'word': 'w1', 'word_actual': 'w1', 'word_language': 'Russian'},
            {'word': 'w2', 'word_actual': 'w2', 'word_language': 'Russian'},
            {'word': 'w3', 'word_actual': 'w3', 'word_language': 'Russian'}]

        morphemes = [
            [
                {'morpheme': 'lem1',
                 'gloss_raw': 'PST:SG:F:IRREFL:IPFV',
                 'pos_raw': 'V',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': None}
            ],
            [
                {'morpheme': 'lem2',
                 'gloss_raw': 'NOM:SG',
                 'pos_raw': 'PRO-DEM-NOUN',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': None}
            ],
            [
                {'morpheme': 'lem3',
                 'gloss_raw': 'PCL',
                 'pos_raw': 'PCL',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': None}
            ]
        ]
        desired_output = [(utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)
