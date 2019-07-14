import os
import unittest

import acqdiv
from acqdiv.parsers.corpora.main.indonesian.IndonesianSessionParser import \
    IndonesianSessionParser


class TestIndonesianParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        toolbox_path = os.path.join(
            here,
            'tests/unittests/corpora/main/indonesian/test_files/Indonesian.txt')

        metadata_path = os.path.join(
            here,
            'tests/unittests/corpora/main/indonesian/test_files/Indonesian.xml')

        cls.parser = IndonesianSessionParser(toolbox_path, metadata_path)

    def test_get_session_metadata(self):
        session = self.parser.parse()
        actual_output = {
            'source_id': session.source_id,
            'Date': session.date
        }

        desired_output = {
            'source_id': 'Indonesian',
            'Date': 'Date',
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        session = self.parser.parse()
        speaker = session.speakers[0]
        actual_output = {
            'age': speaker.age_raw,
            'birthday': speaker.birth_date,
            'id': speaker.code,
            'language': speaker.languages_spoken,
            'name': speaker.name,
            'role': speaker.role_raw,
            'sex': speaker.gender_raw
        }
        desired_output = {
            'age': 'age',
            'birthday': 'birthday',
            'id': 'id',
            'language': 'language',
            'name': 'name',
            'role': 'role',
            'sex': 'sex'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance(self):
        actual_output = list(self.parser.next_utterance())

        utterance = {
            'source_id': 'source_id',
            'start_raw': 'start_raw',
            'end_raw': '',
            'speaker_label': 'speaker_label',
            'addressee': '',
            'childdirected': '',
            'utterance_raw': 'w(ord)1 w2.',
            'utterance': 'w(ord)1 w2',
            'sentence_type': 'default',
            'comment': '',
            'warning': '',
            'morpheme': 'w1pfxseg- w1stemseg -w1sfxseg w2stemseg',
            'gloss_raw': 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            'pos_raw': '',
            'translation': 'This is the translation.'}

        words = [
            {'word': 'w1',
             'word_actual': 'w1',
             'word_target': 'word1',
             'word_language': ''},
            {'word': 'w2',
             'word_actual': 'w2',
             'word_target': 'w2',
             'word_language': ''}]

        morphemes = [
            [
                {'morpheme': 'w1pfxseg-',
                 'gloss_raw': 'w1pfxgloss-',
                 'pos_raw': '',
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': '',
                 'lemma_id': ''},
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': '',
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': '',
                 'lemma_id': ''},
                {'morpheme': '-w1sfxseg',
                 'gloss_raw': '-w1sfxgloss',
                 'pos_raw': '',
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': '',
                 'lemma_id': ''}],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': '',
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': '',
                 'lemma_id': ''}]]
        desired_output = [(utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)
