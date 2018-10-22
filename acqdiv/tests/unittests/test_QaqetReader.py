import unittest

from acqdiv.parsers.toolbox.readers.QaqetReader import QaqetReader as Qr


class TestQaqetReader(unittest.TestCase):

    # ---------- remove_events_utterance ----------

    def test_remove_events_utterance_once(self):
        utterance = '[sound]'
        actual_output = Qr.remove_events_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_utterance_several(self):
        utterance = '[sound][laugh]'
        actual_output = Qr.remove_events_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_utterance_xxx(self):
        utterance = '[x]'
        actual_output = Qr.remove_events_utterance(utterance)
        desired_output = '[x]'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_utterance_x_event(self):
        utterance = 'Hello [x] why [laugh] do you laugh'
        actual_output = Qr.remove_events_utterance(utterance)
        desired_output = 'Hello [x] why do you laugh'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_punctuation ----------

    def test_remove_punctuation_comma(self):
        utterance = 'here , comma'
        actual_output = Qr.remove_punctuation(utterance)
        desired_output = 'here comma'
        self.assertEqual(actual_output, desired_output)

    def test_remove_punctuation_question_mark(self):
        utterance = 'hä?'
        actual_output = Qr.remove_punctuation(utterance)
        desired_output = 'hä'
        self.assertEqual(actual_output, desired_output)

    def test_remove_punctuation_question_dots(self):
        utterance = 'what.. I do'
        actual_output = Qr.remove_punctuation(utterance)
        desired_output = 'what I do'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed ----------

    def test_null_untranscribed_utterance(self):
        utterance = '[x]'
        actual_output = Qr.null_untranscribed_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_utterance_transcribed(self):
        utterance = 'Hello world'
        actual_output = Qr.null_untranscribed_utterance(utterance)
        desired_output = 'Hello world'
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_utterance_unk_in_between(self):
        utterance = 'Hello [x]'
        actual_output = Qr.null_untranscribed_utterance(utterance)
        desired_output = 'Hello [x]'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknown ----------

    def test_unify_unknown(self):
        utterance = 'Hello [x]'
        actual_output = Qr.unify_unknowns_utterance(utterance)
        desired_output = 'Hello ???'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_utterance ----------

    def test_clean_utterance(self):
        utterance = 'Hello.. [x] , how [laugh] are you?'
        actual_output = Qr.clean_utterance(utterance)
        desired_output = 'Hello ??? how are you'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_morpheme_sep ----------

    def test_remove_morpheme_sep_sfx(self):
        morpheme = '-mor'
        actual_output = Qr.remove_morpheme_sep(morpheme)
        desired_output = 'mor'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morpheme_sep_pfx(self):
        morpheme = 'mor-'
        actual_output = Qr.remove_morpheme_sep(morpheme)
        desired_output = 'mor'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morpheme_sep_clitic_sfx(self):
        morpheme = '=mor'
        actual_output = Qr.remove_morpheme_sep(morpheme)
        desired_output = 'mor'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morpheme_sep_clitic_pfx(self):
        morpheme = 'mor='
        actual_output = Qr.remove_morpheme_sep(morpheme)
        desired_output = 'mor'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed_morpheme ----------

    def test_null_untranscribed_morpheme_question_mark(self):
        morpheme = '??'
        actual_output = Qr.null_untranscribed_morpheme(morpheme)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morpheme_stars(self):
        morpheme = '***'
        actual_output = Qr.null_untranscribed_morpheme(morpheme)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- lang2lang ----------

    def test_lang2lang(self):
        morpheme = 'Q'
        actual_output = Qr.lang2lang(morpheme)
        desired_output = 'Qaqet'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_lang ----------

    def test_clean_lang(self):
        morpheme = 'Q='
        actual_output = Qr.clean_lang(morpheme)
        desired_output = 'Qaqet'
        self.assertEqual(actual_output, desired_output)
