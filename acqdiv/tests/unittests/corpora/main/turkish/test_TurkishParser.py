import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.turkish.TurkishCleaner \
    import TurkishCleaner
from acqdiv.parsers.corpora.main.turkish.TurkishSessionParser \
    import TurkishSessionParser
from acqdiv.parsers.corpora.main.turkish.TurkishReader \
    import TurkishReader


class TestTurkishParser(unittest.TestCase):

    def setUp(self):
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader. (Sesotho)"""
        session_str = '*GRA:\tne ?\n%add:\tMOT\n@End'
        actual_reader = TurkishSessionParser.get_reader(
            io.StringIO(session_str))
        self.assertTrue(isinstance(actual_reader, TurkishReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Sesotho)"""
        actual_cleaner = TurkishSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, TurkishCleaner))

    def test_parse(self):
        """Test parse()."""
        session_str = ('*BAB:\tinmekmi istiyo(r)sun ?\n'
                       '%add:\tCHI\n'
                       '%xmor:\tV|in-INF-QUE V|iste-IPFV-2S ?\n'
                       '@End')
        parser = TurkishSessionParser(self.dummy_cha_path)
        parser.reader = TurkishReader(io.StringIO(session_str))
        session = parser.parse()
        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'BAB',
            utt.addressee == 'CHI',
            utt.utterance_raw == 'inmekmi istiyo(r)sun ?',
            utt.utterance == 'inmekmi istiyosun',
            utt.translation == '',
            utt.morpheme_raw == 'V|in-INF-QUE V|iste-IPFV-2S ?',
            utt.gloss_raw == 'V|in-INF-QUE V|iste-IPFV-2S ?',
            utt.pos_raw == 'V|in-INF-QUE V|iste-IPFV-2S ?',
            utt.sentence_type == 'question',
            utt.start_raw == '',
            utt.end_raw == '',
            utt.comment == '',
            utt.warning == ''
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word_language == 'Turkish',
            w1.word == 'inmekmi',
            w1.word_actual == 'inmekmi',
            w1.word_target == 'inmekmi',
            w1.warning == '',
            w2.word_language == 'Turkish',
            w2.word == 'istiyosun',
            w2.word_actual == 'istiyosun',
            w2.word_target == 'istiyorsun',
            w2.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]
        m3 = utt.morphemes[0][2]
        m4 = utt.morphemes[1][0]
        m5 = utt.morphemes[1][1]
        m6 = utt.morphemes[1][2]

        morphemes = [
            m1.gloss_raw == '',
            m1.morpheme == 'in',
            m1.morpheme_language == '',
            m1.pos_raw == 'V',

            m2.gloss_raw == 'INF',
            m2.morpheme == '',
            m2.morpheme_language == '',
            m2.pos_raw == 'sfx',

            m3.gloss_raw == 'QUE',
            m3.morpheme == '',
            m3.morpheme_language == '',
            m3.pos_raw == 'sfx',

            m4.gloss_raw == '',
            m4.morpheme == 'iste',
            m4.morpheme_language == '',
            m4.pos_raw == 'V',

            m5.gloss_raw == 'IPFV',
            m5.morpheme == '',
            m5.morpheme_language == '',
            m5.pos_raw == 'sfx',

            m6.gloss_raw == '2S',
            m6.morpheme == '',
            m6.morpheme_language == '',
            m6.pos_raw == 'sfx'
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
