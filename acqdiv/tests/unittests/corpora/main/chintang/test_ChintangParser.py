import os
import unittest

import acqdiv
from acqdiv.parsers.corpora.main.chintang.session_parser import \
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

    def test_add_session_metadata(self):
        session = self.parser.parse()
        actual_output = {
            'source_id': session.source_id,
            'date': session.date,
            'media_type': session.media_filename
        }
        desired_output = {
            'source_id': 'Chintang',
            'date': 'session date',
            'media_type': ''
        }
        self.assertEqual(actual_output, desired_output)

    def test_add_speakers(self):
        session = self.parser.parse()
        speaker = session.speakers[0]

        actual_output = {
            'role': speaker.role_raw,
            'name': speaker.name,
            'code': speaker.code,
            'languages': speaker.languages_spoken,
            'age': speaker.age_raw,
            'birthdate': speaker.birth_date,
            'sex': speaker.gender_raw,
        }

        desired_output = {
            'role': 'actor family social role',
            'name': 'actor name',
            'code': 'MAR',
            'languages': 'actor language id',
            'age': 'actor age',
            'birthdate': 'actor birthdate',
            'sex': 'actor sex',
        }
        self.assertEqual(actual_output, desired_output)

    def test_add_record(self):
        session = self.parser.parse()

        utt = session.utterances[-1]

        actual_utterance = {
            'source_id': utt.source_id,
            'start_raw': utt.start_raw,
            'end_raw': utt.end_raw,
            'speaker_label': utt.speaker.code,
            'addressee': utt.addressee,
            'childdirected': utt.childdirected,
            'utterance_raw': utt.utterance_raw,
            'utterance': utt.utterance,
            'sentence_type': utt.sentence_type,
            'comment': utt.comment,
            'warning': utt.warning,
            'morpheme': utt.morpheme_raw,
            'gloss_raw': utt.gloss_raw,
            'pos_raw': utt.pos_raw,
            'translation': utt.translation
        }

        desired_utterance = {
            'source_id': 'session_name.001',
            'start_raw': '00:50:11.150',
            'end_raw': '00:50:22.350',
            'speaker_label': 'MAR',
            'addressee': None,
            'childdirected': True,
            'utterance_raw': 'w1 w2',
            'utterance': 'w1 w2',
            'sentence_type': 'question',
            'comment': '',
            'warning': '',
            'morpheme': 'w1pfxseg- w1stemseg -w1sfxseg w2stemseg',
            'gloss_raw': 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            'pos_raw': 'w1pfxpos- w1stempos -w1sfxpos w2stempos',
            'translation': 'This is the translation.'}

        w1 = utt.words[0]
        w2 = utt.words[1]

        actual_words = [
            {'word': w1.word,
             'word_actual': w1.word_actual,
             'word_language': w1.word_language,
             'word_target': w1.word_target,
             },
            {'word': w2.word,
             'word_actual': w2.word_actual,
             'word_language': w2.word_language,
             'word_target': w2.word_target,
             }
        ]

        desired_words = [
            {'word': 'w1',
             'word_actual': 'w1',
             'word_language': '',
             'word_target': '',
             },
            {'word': 'w2',
             'word_actual': 'w2',
             'word_language': '',
             'word_target': '',
             }
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]
        m3 = utt.morphemes[0][2]
        m4 = utt.morphemes[1][0]

        actual_morphemes = [
            [
                {'morpheme': m1.morpheme,
                 'gloss_raw': m1.gloss_raw,
                 'pos_raw': m1.pos_raw,
                 'morpheme_language': m1.morpheme_language,
                 'lemma_id': m1.lemma_id,
                 'type': m1.type,
                 'warning': m1.warning},
                {'morpheme': m2.morpheme,
                 'gloss_raw': m2.gloss_raw,
                 'pos_raw': m2.pos_raw,
                 'morpheme_language': m2.morpheme_language,
                 'lemma_id': m2.lemma_id,
                 'type': m2.type,
                 'warning': m2.warning},
                {'morpheme': m3.morpheme,
                 'gloss_raw': m3.gloss_raw,
                 'pos_raw': m3.pos_raw,
                 'morpheme_language': m3.morpheme_language,
                 'lemma_id': m3.lemma_id,
                 'type': m3.type,
                 'warning': m3.warning}],
            [
                {'morpheme': m4.morpheme,
                 'gloss_raw': m4.gloss_raw,
                 'pos_raw': m4.pos_raw,
                 'morpheme_language': m4.morpheme_language,
                 'lemma_id': m4.lemma_id,
                 'type': m4.type,
                 'warning': m4.warning}]]

        desired_morphemes = [
            [
                {'morpheme': 'w1pfxseg',
                 'gloss_raw': 'w1pfxgloss',
                 'pos_raw': 'w1pfxpos',
                 'morpheme_language': 'Chintang',
                 'lemma_id': 'w1pfxID',
                 'type': 'target',
                 'warning': ''},
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': 'w1stempos',
                 'morpheme_language': 'Chintang',
                 'lemma_id': 'w1stemID',
                 'type': 'target',
                 'warning': ''},
                {'morpheme': 'w1sfxseg',
                 'gloss_raw': 'w1sfxgloss',
                 'pos_raw': 'w1sfxpos',
                 'morpheme_language': 'Chintang',
                 'lemma_id': 'w1sfxID',
                 'type': 'target',
                 'warning': ''}],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': 'w2stempos',
                 'morpheme_language': 'Nepali',
                 'lemma_id': 'w2stemID',
                 'type': 'target',
                 'warning': ''}]]

        actual_output = [
            (actual_utterance, actual_words, actual_morphemes)
        ]
        desired_output = [
            (desired_utterance, desired_words, desired_morphemes)]
        self.assertEqual(actual_output, desired_output)
