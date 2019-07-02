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
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'Cname': 'Indonesian',
            'Corpus': 'Corpus',
            'Date': 'Date',
            'Id': 'Id',
            'Lang': 'Lang',
            'PID': 'PID'}
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        actual_output = next(self.parser.next_speaker())
        desired_output = {
            'age': 'age',
            'birthday': 'birthday',
            'id': 'id',
            'language': 'language',
            'name': 'name',
            'role': 'role',
            'sex': 'sex'}
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance(self):
        actual_output = list(self.parser.next_utterance())

        utterance = {
            'source_id': 'source_id',
            'start_raw': 'start_raw',
            'end_raw': None,
            'speaker_label': 'speaker_label',
            'addressee': None,
            'childdirected': None,
            'utterance_raw': 'w(ord)1 w2.',
            'utterance': 'w(ord)1 w2',
            'sentence_type': 'default',
            'comment': None,
            'warning': None,
            'morpheme': 'w1pfxseg- w1stemseg -w1sfxseg w2stemseg',
            'gloss_raw': 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            'pos_raw': None,
            'translation': 'This is the translation.'}

        words = [
            {'word': 'w1', 'word_actual': 'w1', 'word_target': 'word1',
             'word_language': 'Indonesian'},
            {'word': 'w2', 'word_actual': 'w2', 'word_target': 'w2',
             'word_language': 'Indonesian'}]

        morphemes = [
            [
                {'morpheme': 'w1pfxseg-',
                 'gloss_raw': 'w1pfxgloss-',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': None},
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': None},
                {'morpheme': '-w1sfxseg',
                 'gloss_raw': '-w1sfxgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': None}],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'type': 'target',
                 'warning': None}]]
        desired_output = [(None, None, None),
                          (None, None, None),
                          (utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)
