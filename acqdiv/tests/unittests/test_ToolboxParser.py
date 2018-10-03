import unittest
from acqdiv.parsers.toolbox.ToolboxParser import *
from acqdiv.parsers.parsers import CorpusConfigParser


###############################################################################


class TestChintangParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = CorpusConfigParser()
        config.read('../../ini/Chintang.ini')
        file_path = 'test_files/Chintang.txt'
        cls.parser = ChintangParser(config, file_path)

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

###############################################################################


class TestIndonesianParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = CorpusConfigParser()
        config.read('../../ini/Indonesian.ini')
        file_path = 'test_files/Indonesian.txt'
        cls.parser = IndonesianParser(config, file_path)

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
                 'lemma_id': None,
                 'type': 'target',
                 'warning': None},
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'lemma_id': None,
                 'type': 'target',
                 'warning': None},
                {'morpheme': '-w1sfxseg',
                 'gloss_raw': '-w1sfxgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'lemma_id': None,
                 'type': 'target',
                 'warning': None}],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': None,
                 'morpheme_language': 'Indonesian',
                 'lemma_id': None,
                 'type': 'target',
                 'warning': None}]]
        desired_output = [(None, None, None),
                          (None, None, None),
                          (utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestRussianParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = CorpusConfigParser()
        config.read('../../ini/Russian.ini')
        file_path = 'test_files/Russian.txt'
        cls.parser = RussianParser(config, file_path)

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
                 'lemma_id': None,
                 'type': 'actual',
                 'warning': None}
            ],
            [
                {'morpheme': 'lem2',
                 'gloss_raw': 'NOM:SG',
                 'pos_raw': 'PRO-DEM-NOUN',
                 'morpheme_language': 'Russian',
                 'lemma_id': None,
                 'type': 'actual',
                 'warning': None}
            ],
            [
                {'morpheme': 'lem3',
                 'gloss_raw': 'PCL',
                 'pos_raw': 'PCL',
                 'morpheme_language': 'Russian',
                 'lemma_id': None,
                 'type': 'actual',
                 'warning': None}
            ]
        ]
        desired_output = [(utterance, words, morphemes)]
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
