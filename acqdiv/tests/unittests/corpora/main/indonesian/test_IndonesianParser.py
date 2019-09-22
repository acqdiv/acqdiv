import os
import unittest

import acqdiv
from acqdiv.parsers.corpora.main.indonesian.session_parser import \
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

    def test_session_metadata(self):
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

    def test_speakers(self):
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
            'id': 'spe',
            'language': 'language',
            'name': 'name',
            'role': 'role',
            'sex': 'sex'
        }
        self.assertEqual(actual_output, desired_output)

    def test_records(self):
        session = self.parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'source_id',
            utt.start_raw == 'start_raw',
            utt.end_raw == '',
            utt.speaker.code == 'spe',
            utt.addressee is None,
            utt.childdirected == '',
            utt.utterance_raw == 'w(ord)1 w2.',
            utt.utterance == 'w(ord)1 w2',
            utt.sentence_type == 'default',
            utt.comment == '',
            utt.warning == '',
            utt.morpheme_raw == 'w1pfxseg- w1stemseg -w1sfxseg w2stemseg',
            utt.gloss_raw == 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            utt.pos_raw == 'w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss',
            utt.translation == 'This is the translation.'
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word == 'w1',
            w1.word_actual == 'w1',
            w1.word_target == 'word1',
            w1.word_language == '',

            w2.word == 'w2',
            w2.word_actual == 'w2',
            w2.word_target == 'w2',
            w2.word_language == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]
        m3 = utt.morphemes[0][2]
        m4 = utt.morphemes[1][0]

        morphemes = [
            m1.morpheme == 'w1pfxseg',
            m1.gloss_raw == 'w1pfxgloss',
            m1.pos_raw == 'w1pfxgloss',
            m1.morpheme_language == 'Indonesian',
            m1.type == 'target',
            m1.warning == '',
            m1.lemma_id == '',

            m2.morpheme == 'w1stemseg',
            m2.gloss_raw == 'w1stemgloss',
            m2.pos_raw == 'w1stemgloss',
            m2.morpheme_language == 'Indonesian',
            m2.type == 'target',
            m2.warning == '',
            m2.lemma_id == '',

            m3.morpheme == 'w1sfxseg',
            m3.gloss_raw == 'w1sfxgloss',
            m3.pos_raw == 'w1sfxgloss',
            m3.morpheme_language == 'Indonesian',
            m3.type == 'target',
            m3.warning == '',
            m3.lemma_id == '',

            m4.morpheme == 'w2stemseg',
            m4.gloss_raw == 'w2stemgloss',
            m4.pos_raw == 'w2stemgloss',
            m4.morpheme_language == 'Indonesian',
            m4.type == 'target',
            m4.warning == '',
            m4.lemma_id == ''
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
