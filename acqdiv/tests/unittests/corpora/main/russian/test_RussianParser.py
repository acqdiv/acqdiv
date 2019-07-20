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

    def test_session_metadata(self):
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

    def test_speakers(self):
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

    def test_records(self):
        session = self.parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'source_id',
            utt.start_raw == 'start_raw',
            utt.end_raw == 'end_raw',
            utt.speaker_label == 'speaker_label',
            utt.addressee == '',
            utt.childdirected == '',
            utt.utterance_raw == 'w1 "," w2 w3 .',
            utt.utterance == 'w1 w2 w3',
            utt.sentence_type == 'default',
            utt.translation == '',
            utt.comment == '',
            utt.warning == '',
            utt.morpheme == 'lem1 "," lem2 lem3 .',
            utt.gloss_raw == 'V-PST:SG:F:IRREFL:IPFV PUNCT '
                             'PRO-DEM-NOUN:NOM:SG PCL PUNCT',
            utt.pos_raw == 'V-PST:SG:F:IRREFL:IPFV PUNCT '
                           'PRO-DEM-NOUN:NOM:SG PCL PUNCT'
            ]

        w1 = utt.words[0]
        w2 = utt.words[1]
        w3 = utt.words[2]

        words = [
            w1.word == 'w1',
            w1.word_actual == 'w1',
            w1.word_target == '',
            w1.word_language == '',

            w2.word == 'w2',
            w2.word_actual == 'w2',
            w2.word_target == '',
            w2.word_language == '',

            w3.word == 'w3',
            w3.word_actual == 'w3',
            w3.word_target == '',
            w3.word_language == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[1][0]
        m3 = utt.morphemes[2][0]

        morphemes = [
            m1.morpheme == 'lem1',
            m1.gloss_raw == 'PST:SG:F:IRREFL:IPFV',
            m1.pos_raw == 'V',
            m1.morpheme_language == 'Russian',
            m1.type == 'actual',
            m1.warning == '',
            m1.lemma_id == '',

            m2.morpheme == 'lem2',
            m2.gloss_raw == 'NOM:SG',
            m2.pos_raw == 'PRO-DEM-NOUN',
            m2.morpheme_language == 'Russian',
            m2.type == 'actual',
            m2.warning == '',
            m2.lemma_id == '',

            m3.morpheme == 'lem3',
            m3.gloss_raw == 'PCL',
            m3.pos_raw == 'PCL',
            m3.morpheme_language == 'Russian',
            m3.type == 'actual',
            m3.warning == '',
            m3.lemma_id == ''

        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
