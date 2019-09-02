import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.cree.cleaner import CreeCleaner
from acqdiv.parsers.corpora.main.cree.session_parser \
    import CreeSessionParser
from acqdiv.parsers.corpora.main.cree.reader import CreeReader


class TestCreeParser(unittest.TestCase):
    """Class to test the CreeSessionParser."""

    def setUp(self):
        self.maxDiff = None
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

    def test_get_reader(self):
        """Test get_reader. (Cree)"""
        session_str = ('*CHI:\tchair . 2883660_2884622\n%pho:\t*\n%mod:\t*\n'
                       '%eng:\tohhhhhh\n@End')
        actual_reader = CreeSessionParser.get_reader(io.StringIO(session_str))
        self.assertTrue(isinstance(actual_reader, CreeReader))

    def test_get_cleaner(self):
        """Test get_cleaner. (Cree)"""
        actual_cleaner = CreeSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, CreeCleaner))

    def test_parse_no_misalignments_single_word(self):
        """Test parse() with no misalignments."""
        session_str = ('*CHI:\tchair . 2883660_2884622\n'
                       '%pho:\t*\n'
                       '%mod:\t*\n'
                       '%eng:\tohhhhhh\n'
                       '@End')
        parser = CreeSessionParser(self.dummy_cha_path)
        parser.reader = CreeReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'CHI',
            utt.addressee == '',
            utt.utterance_raw == 'chair .',
            utt.utterance == 'chair',
            utt.translation == 'ohhhhhh',
            utt.morpheme_raw == '',
            utt.gloss_raw == '',
            utt.pos_raw == '',
            utt.sentence_type == 'default',
            utt.start_raw == '2883660',
            utt.end_raw == '2884622',
            utt.comment == '',
            utt.warning == ''
        ]

        w = utt.words[0]

        words = [
            w.word_language == '',
            w.word == 'chair',
            w.word_actual == 'chair',
            w.word_target == 'chair',
            w.warning == ''
        ]

        assert (False not in utterance
                and False not in words
                and len(utt.morphemes) == 0)

    def test_parse_no_misalignments_multiple_words(self):
        """Test parse() with no misalignemnts."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n'
                       '%pho:\t‹wo ni›\n'
                       '%mod:\t‹ˈwo *›\n'
                       '%eng:\tegg me\n'
                       '%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n'
                       '%xtarmor:\t[wo *]\n'
                       '%xmormea:\t[egg 1]\n'
                       '@End')
        parser = CreeSessionParser(self.dummy_cha_path)
        parser.reader = CreeReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'CHI',
            utt.addressee == '',
            utt.utterance_raw == '‹wâu nîyi› .',
            utt.utterance == 'wâu nîyi',
            utt.translation == 'egg me',
            utt.morpheme_raw == '[wo *]',
            utt.gloss_raw == '[egg 1]',
            utt.pos_raw == '[ni pro]',
            utt.sentence_type == 'default',
            utt.start_raw == '1198552',
            utt.end_raw == '1209903',
            utt.comment == '',
            utt.warning == ''
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word_language == '',
            w1.word == 'wâu',
            w1.word_actual == 'wâu',
            w1.word_target == 'wâu',
            w1.warning == '',
            w2.word_language == '',
            w2.word == 'nîyi',
            w2.word_actual == 'nîyi',
            w2.word_target == 'nîyi',
            w2.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[1][0]

        morphemes = [
            m1.gloss_raw == 'egg',
            m1.morpheme == 'wo',
            m1.morpheme_language == 'Cree',
            m1.pos_raw == 'ni',
            m2.gloss_raw == '1',
            m2.morpheme == '',
            m2.morpheme_language == 'Cree',
            m2.pos_raw == 'pro'
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)

    def test_parse_records_mm_misalignments_1(self):
        """Test parse() with more glosses/POS tags than segments."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n'
                       '%pho:\t‹wo ni›\n'
                       '%mod:\t‹ˈwo›\n'
                       '%eng:\tegg me\n'
                       '%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n'
                       '%xtarmor:\t[wo]\n'
                       '%xmormea:\t[egg 1]\n'
                       '@End')
        parser = CreeSessionParser(self.dummy_cha_path)
        parser.reader = CreeReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'CHI',
            utt.addressee == '',
            utt.utterance_raw == '‹wâu nîyi› .',
            utt.utterance == 'wâu nîyi',
            utt.translation == 'egg me',
            utt.morpheme_raw == '[wo]',
            utt.gloss_raw == '[egg 1]',
            utt.pos_raw == '[ni pro]',
            utt.sentence_type == 'default',
            utt.start_raw == '1198552',
            utt.end_raw == '1209903',
            utt.comment == '',
            utt.warning == ''
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word_language == '',
            w1.word == 'wâu',
            w1.word_actual == 'wâu',
            w1.word_target == 'wâu',
            w1.warning == '',

            w2.word_language == '',
            w2.word == 'nîyi',
            w2.word_actual == 'nîyi',
            w2.word_target == 'nîyi',
            w2.warning == ''
        ]

        m = utt.morphemes[0][0]

        morphemes = [
            m.gloss_raw == '',
            m.morpheme == 'wo',
            m.morpheme_language == 'Cree',
            m.pos_raw == ''
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)

    def test_parse_records_mm_misalignments_2(self):
        """Test parse() with too few POS tags."""

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n'
                       '%pho:\t‹wo ni›\n'
                       '%eng:\tegg me\n'
                       '%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[pro]\n'
                       '%xtarmor:\t[wo ni]\n'
                       '%xmormea:\t[egg 1]\n'
                       '@End')
        parser = CreeSessionParser(self.dummy_cha_path)
        parser.reader = CreeReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'CHI',
            utt.addressee == '',
            utt.utterance_raw == '‹wâu nîyi› .',
            utt.utterance == 'wâu nîyi',
            utt.translation == 'egg me',
            utt.morpheme_raw == '[wo ni]',
            utt.gloss_raw == '[egg 1]',
            utt.pos_raw == '[pro]',
            utt.sentence_type == 'default',
            utt.start_raw == '1198552',
            utt.end_raw == '1209903',
            utt.comment == '',
            utt.warning == ''
        ]

        w1 = utt.words[0]
        w2 = utt.words[1]

        words = [
            w1.word_language == '',
            w1.word == 'wâu',
            w1.word_actual == 'wâu',
            w1.word_target == 'wâu',
            w1.warning == '',

            w2.word_language == '',
            w2.word == 'nîyi',
            w2.word_actual == 'nîyi',
            w2.word_target == 'nîyi',
            w2.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[1][0]

        morphemes = [
            m1.gloss_raw == 'egg',
            m1.morpheme == 'wo',
            m1.morpheme_language == 'Cree',
            m1.pos_raw == '',

            m2.gloss_raw == '1',
            m2.morpheme == 'ni',
            m2.morpheme_language == 'Cree',
            m2.pos_raw == ''
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
