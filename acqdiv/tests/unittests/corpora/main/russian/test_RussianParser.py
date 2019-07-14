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
        session = self.parser.parse()
        actual_output = {
            'source_id': session.source_id,
            'date': session.date,
        }
        desired_output = {
            'source_id': 'Russian',
            'date': 'session date'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        session = self.parser.parse()
        speaker = session.speakers[0]
        actual_output = {
            'role': speaker.role_raw,
            'name': speaker.name,
            'code': speaker.code,
            'age': speaker.age_raw,
            'birthdate': speaker.birth_date,
            'sex': speaker.gender_raw,
        }
        desired_output = {
            'role': 'actor family social role',
            'name': 'actor name',
            'code': 'actor code',
            'age': 'actor age',
            'birthdate': 'actor birthdate',
            'sex': 'actor sex'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance(self):
        actual_output = list(self.parser.next_utterance())

        utterance = {
            'source_id': 'source_id',
            'start_raw': 'start_raw',
            'end_raw': 'end_raw',
            'speaker_label': 'speaker_label',
            'addressee': '',
            'childdirected': '',
            'utterance_raw': 'w1 "," w2 w3 .',
            'utterance': 'w1 w2 w3',
            'sentence_type': 'default',
            'translation': '',
            'comment': '',
            'warning': '',
            'morpheme': 'lem1 "," lem2 lem3 .',
            'gloss_raw': 'V-PST:SG:F:IRREFL:IPFV PUNCT PRO-DEM-NOUN:NOM:SG '
                         'PCL PUNCT',
            'pos_raw': 'V-PST:SG:F:IRREFL:IPFV PUNCT PRO-DEM-NOUN:NOM:SG PCL '
                       'PUNCT'}

        words = [
            {'word': 'w1',
             'word_actual': 'w1',
             'word_target': '',
             'word_language': ''
             },
            {'word': 'w2',
             'word_actual': 'w2',
             'word_target': '',
             'word_language': '',
             },
            {'word': 'w3',
             'word_actual': 'w3',
             'word_target': '',
             'word_language': ''}]

        morphemes = [
            [
                {'morpheme': 'lem1',
                 'gloss_raw': 'PST:SG:F:IRREFL:IPFV',
                 'pos_raw': 'V',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': '',
                 'lemma_id': ''}
            ],
            [
                {'morpheme': 'lem2',
                 'gloss_raw': 'NOM:SG',
                 'pos_raw': 'PRO-DEM-NOUN',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': '',
                 'lemma_id': ''}
            ],
            [
                {'morpheme': 'lem3',
                 'gloss_raw': 'PCL',
                 'pos_raw': 'PCL',
                 'morpheme_language': 'Russian',
                 'type': 'actual',
                 'warning': '',
                 'lemma_id': ''}
            ]
        ]
        desired_output = [(utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)
