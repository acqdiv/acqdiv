import os
import unittest

import acqdiv
from acqdiv.parsers.corpora.main.chintang.ChintangSessionParser import \
    ChintangSessionParser


class TestChintangParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        toolbox_path = os.path.join(
            here,
            'tests/unittests/corpora/main/chintang/test_files/Chintang.txt')

        metadata_path = os.path.join(
            here,
            'tests/unittests/corpora/main/chintang/test_files/Chintang.imdi')

        cls.parser = ChintangSessionParser(toolbox_path, metadata_path)

    def test_get_session_metadata(self):
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'id': 'Chintang',
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
            'role': 'actor family social role',
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
            'source_id': 'session_name.001',
            'start_raw': '00:50:11.150',
            'end_raw': '00:50:22.350',
            'speaker_label': 'MAR',
            'addressee': None,
            'childdirected': True,
            'utterance_raw': 'w1 w2',
            'utterance': 'w1 w2',
            'sentence_type': 'question',
            'comment': None,
            'warning': None,
            'lemma_id': 'w1pfxID- w1stemID -w1sfxID w2stemID',
            'morpheme': 'w1pfxseg- w1stemseg -w1sfxseg w2stemseg',
            'gloss_raw': 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            'pos_raw': 'w1pfxpos- w1stempos -w1sfxpos w2stempos',
            'translation': 'This is the translation.'}

        words = [
            {'word': 'w1', 'word_actual': 'w1', 'word_language': 'Chintang'},
            {'word': 'w2', 'word_actual': 'w2', 'word_language': 'Nepali'}]

        morphemes = [
            [
                {'morpheme': 'w1pfxseg-',
                 'gloss_raw': 'w1pfxgloss-',
                 'pos_raw': 'w1pfxpos-',
                 'morpheme_language': 'Chintang',
                 'lemma_id': 'w1pfxID-',
                 'type': 'target',
                 'warning': None},
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': 'w1stempos',
                 'morpheme_language': 'Chintang',
                 'lemma_id': 'w1stemID',
                 'type': 'target',
                 'warning': None},
                {'morpheme': '-w1sfxseg',
                 'gloss_raw': '-w1sfxgloss',
                 'pos_raw': '-w1sfxpos',
                 'morpheme_language': 'Chintang',
                 'lemma_id': '-w1sfxID',
                 'type': 'target',
                 'warning': None}],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': 'w2stempos',
                 'morpheme_language': 'Nepali',
                 'lemma_id': 'w2stemID',
                 'type': 'target',
                 'warning': None}]]
        desired_output = [(utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)
