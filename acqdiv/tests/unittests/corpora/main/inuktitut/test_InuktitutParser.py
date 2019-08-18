import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.inuktitut.InuktitutCleaner import \
    InuktitutCleaner
from acqdiv.parsers.corpora.main.inuktitut.InuktitutSessionParser import \
    InuktitutSessionParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutReader import \
    InuktitutReader


class TestInuktitutParser(unittest.TestCase):
    """Class to test InuktitutSessionParser."""

    def setUp(self):
        self.maxDiff = None
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

    def test_get_reader(self):
        """Test get_reader for Inuktitutparser."""
        actual_reader = InuktitutSessionParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, InuktitutReader))

    def test_get_cleaner(self):
        """Test get_cleaner for Inuktitutparser."""
        actual_cleaner = InuktitutSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, InuktitutCleaner))

    def test_parse(self):
        """Test parse()."""
        session_str = (
            '*MAE:\tAllaigutama  .\n'
            '%eng:\tGive me a comb  .\n'
            '%xmor:\tNR|ollaoguto^comb+NI|mim^MOD_SG .\n'
            '%tim:\t00:01:32\n'
            '%add:\tRO\n'
            '@End'
        )
        parser = InuktitutSessionParser(self.dummy_cha_path)
        parser.reader = InuktitutReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'MAE',
            utt.addressee == 'RO',
            utt.utterance_raw == 'Allaigutama  .',
            utt.utterance == 'Allaigutama',
            utt.translation == 'Give me a comb  .',
            utt.morpheme_raw == 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            utt.gloss_raw == 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            utt.pos_raw == 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            utt.sentence_type == 'default',
            utt.start_raw == '00:01:32',
            utt.end_raw == '',
            utt.comment == '',
            utt.warning == ''
        ]

        w = utt.words[0]

        words = [
            w.word_language == '',
            w.word == 'Allaigutama',
            w.word_actual == 'Allaigutama',
            w.word_target == 'Allaigutama',
            w.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]

        morphemes = [
            m1.morpheme_language == 'Inuktitut',
            m1.morpheme == 'ollaoguto',
            m1.gloss_raw == 'comb',
            m1.pos_raw == 'NR',

            m2.morpheme_language == 'Inuktitut',
            m2.morpheme == 'mim',
            m2.gloss_raw == 'MOD_SG',
            m2.pos_raw == 'NI'
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
