import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.sesotho.SesothoCleaner import SesothoCleaner
from acqdiv.parsers.corpora.main.sesotho.SesothoSessionParser \
    import SesothoSessionParser
from acqdiv.parsers.corpora.main.sesotho.SesothoReader import SesothoReader


class TestSesothoParser(unittest.TestCase):
    """Class to test the SesothoSessionParser."""

    def setUp(self):
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Sesotho)"""
        actual_reader = SesothoSessionParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, SesothoReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Sesotho)"""
        actual_cleaner = SesothoSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, SesothoCleaner))

    def test_parse(self):
        """Test parse()."""

        session_str = ('*NHM:\te tsamo . 113200_115376\n'
                       '%gls:\te tsamay-a .\n'
                       '%xcod:\tv^leave-m^i .\n'
                       '%eng:\tYes go and\n'
                       '@End')
        parser = SesothoSessionParser(self.dummy_cha_path)
        parser.reader = SesothoReader(io.StringIO(session_str))
        session = parser.parse()
        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'NHM',
            utt.addressee == '',
            utt.utterance_raw == 'e tsamo .',
            utt.utterance == 'e tsamaya',
            utt.translation == 'Yes go and',
            utt.morpheme_raw == 'e tsamay-a .',
            utt.gloss_raw == 'v^leave-m^i .',
            utt.pos_raw == 'v^leave-m^i .',
            utt.sentence_type == 'default',
            utt.start_raw == '113200',
            utt.end_raw == '115376',
            utt.comment == '',
            utt.warning == ''
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word_language == '',
            w1.word == 'e',
            w1.word_actual == 'e',
            w1.word_target == 'e',
            w1.warning == '',
            w2.word_language == '',
            w2.word == 'tsamaya',
            w2.word_actual == 'tsamaya',
            w2.word_target == 'tsamaya',
            w2.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]

        morphemes = [
            m1.gloss_raw == 'v^leave',
            m1.morpheme == '',
            m1.morpheme_language == '',
            m1.pos_raw == 'v',
            m2.gloss_raw == 'm^i',
            m2.morpheme == '',
            m2.morpheme_language == '',
            m2.pos_raw == 'sfx'
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
