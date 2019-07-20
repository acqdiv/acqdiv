import io
import unittest
import os
import acqdiv

from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProSessionParser \
    import JapaneseMiiProSessionParser
from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProReader import \
    JapaneseMiiProReader


class TestJapaneseMiiProParser(unittest.TestCase):
    """Class to test the JapaneseMiiProSessionParser."""

    def setUp(self):
        self.maxDiff = None
        here = os.path.abspath(os.path.dirname(acqdiv.__file__))

        self.dummy_cha_path = os.path.join(
            here,
            'tests/unittests/chat/test_files/dummy.cha')

    def test_get_reader(self):
        """Test get_reader for JapaneseMiiProSessionParser."""
        actual_reader = JapaneseMiiProSessionParser.get_reader(io.StringIO(''))
        self.assertTrue(isinstance(actual_reader, JapaneseMiiProReader))

    def test_get_cleaner(self):
        """Test get_cleaner for JapaneseMiiProSessionParser."""
        actual_cleaner = JapaneseMiiProSessionParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, JapaneseMiiProCleaner))

    def test_parse(self):
        """Test parse()."""
        session_str = ('tom20010724.cha:*MOT:\tdoozo . 4087868_4089193\n'
                       '%xtrn:\tn:prop|Hono-chan co:g|doozo .\n'
                       '%ort:\tホノちゃんどうぞ。\n'
                       '@End')
        parser = JapaneseMiiProSessionParser(self.dummy_cha_path)
        parser.reader = JapaneseMiiProReader(io.StringIO(session_str))
        session = parser.parse()

        utt = session.utterances[0]

        utterance = [
            utt.source_id == 'dummy_0',
            utt.speaker_label == 'MOT',
            utt.addressee == '',
            utt.utterance_raw == 'doozo .',
            utt.utterance == 'doozo',
            utt.translation == '',
            utt.morpheme == 'n:prop|Hono-chan co:g|doozo .',
            utt.gloss_raw == 'n:prop|Hono-chan co:g|doozo .',
            utt.pos_raw == 'n:prop|Hono-chan co:g|doozo .',
            utt.sentence_type == 'default',
            utt.start_raw == '4087868',
            utt.end_raw == '4089193',
            utt.comment == '',
            utt.warning == ''
        ]

        w = utt.words[0]

        words = [
            w.word_language == 'Japanese',
            w.word == 'doozo',
            w.word_actual == 'doozo',
            w.word_target == 'doozo',
            w.warning == ''
        ]

        m1 = utt.morphemes[0][0]
        m2 = utt.morphemes[0][1]
        m3 = utt.morphemes[1][0]

        morphemes = [
            m1.gloss_raw == '',
            m1.morpheme == 'Hono',
            m1.morpheme_language == '',
            m1.pos_raw == 'n:prop',

            m2.gloss_raw == 'chan',
            m2.morpheme == '',
            m2.morpheme_language == '',
            m2.pos_raw == 'sfx',

            m3.gloss_raw == '',
            m3.morpheme == 'doozo',
            m3.morpheme_language == '',
            m3.pos_raw == 'co:g'
        ]

        assert (False not in utterance
                and False not in words
                and False not in morphemes)
