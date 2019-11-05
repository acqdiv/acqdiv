import unittest

from acqdiv.parsers.corpora.main.turkish.cleaner import TurkishCleaner


class TestTurkishCleaner(unittest.TestCase):

    # ---------- single_morph_word ----------

    def test_single_morph_word_underscore(self):
        """Test single_morph_word with an underscore."""
        utterance = 'I have to test'
        morph_tier = 'PRON|I V|have_to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_plus(self):
        """Test single_morph_word with a plus."""
        utterance = 'I have to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_multiple_complexes(self):
        """Test single_morph_word with multiple complexes."""
        utterance = 'I have to test and I have to test'
        morph_tier = 'PRON|I V|have+to V|test CORD|and PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test and I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_join_sep(self):
        """Test single_morph_word with no join separator."""
        utterance = 'I haveto test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_join_sep_at_end(self):
        """Test single_morph_word with no join separator at the end."""
        utterance = 'I haveto'
        morph_tier = 'PRON|I V|have+to'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex(self):
        """Test single_morph_word with no complex."""
        utterance = 'I test'
        morph_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex_misalignment1(self):
        """Test single_morph_word with no complex but with misalignment."""
        utterance = 'I test it'
        morph_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex_misalignment2(self):
        """Test single_morph_word with no complex but with misalignment."""
        utterance = 'I test'
        morph_tier = 'PRON|I V|test PRON|it'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_already_joined(self):
        """Test single_morph_word with already joined complex."""
        utterance = 'I have_to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_empty_mor(self):
        """Test single_morph_word with empty morphology tier."""
        utterance = 'I have_to test'
        morph_tier = ''
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_empty_utterance(self):
        """Test single_morph_word with empty utterance."""
        utterance = ''
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_unsimilar(self):
        """Test single_morph_word with unsimilar wword and mword."""
        utterance = 'I got to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    # ---------- separate_morph_word ----------

    def test_separate_morph_word_underscore(self):
        """Test separate_morph_word with underscore."""
        utterance = 'bla tu_ta bla'
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta bla', 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_plus(self):
        """Test separate_morph_word with plus."""
        utterance = 'bla tu+ta bla'
        mor_tier = 'N|bla V|N|tu+V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta bla', 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_with_suffixes(self):
        """Test separate_morph_word with suffixes."""
        utterance = 'bla tuu_taa bla'
        mor_tier = 'N|bla V|N|tu-U_V|ta-A N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tuu taa bla', 'N|bla N|tu-U V|ta-A N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex(self):
        """Test separate_morph_word with no complex."""
        utterance = 'I test'
        mor_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex_misalignment1(self):
        """Test separate_morph_word with no complex but with misalignment."""
        utterance = 'I test it'
        mor_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex_misalignment2(self):
        """Test separate_morph_word with no complex but with misalignment."""
        utterance = 'I test'
        mor_tier = 'PRON|I V|test PRON|it'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_empty_mor(self):
        """Test separate_morph_word with empty morphology tier."""
        utterance = 'I have_to test'
        mor_tier = ''
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_empty_utterance(self):
        """Test separate_morph_word with empty utterance."""
        utterance = ''
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_multiple_complexes(self):
        """Test separate_morph_word with multiple complexes."""
        utterance = 'bla tu+ta tu_ta'
        mor_tier = 'N|bla V|N|tu_V|ta V|N|tu+V|ta'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta tu ta', 'N|bla N|tu V|ta N|tu V|ta'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_join_sep(self):
        """Test separate_morph_word with no join separator."""
        utterance = 'bla tuta bla'
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    # unify_untranscribed

    def test_unify_untranscribed_xxx_start(self):
        """Test with `xxx` at the start of utterance."""
        utterance = 'xxx great'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '??? great'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_xxx_end(self):
        """Test with `xxx` at the end of utterance."""
        utterance = 'This is xxx'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This is ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_xxx_within(self):
        """Test with `xxx` within utterance."""
        utterance = 'This xxx great'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? great'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_five_y(self):
        """Test with five `y`s."""
        utterance = 'yyyyy'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_within_word(self):
        """Test `yyy` occurring in word."""
        utterance = 'yyyia'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'yyyia'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_terminator(self):
        """Test `yyy` with terminator."""
        utterance = 'yyy.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_multiple_yyy(self):
        """Test multiple `yyy`s."""
        utterance = 'This yyy yyy good'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? ??? good'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_scoped(self):
        """Test `yyy` within scoping."""
        utterance = 'This <yyy good> [=! good]'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This <??? good> [=! good]'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_ww(self):
        """Test `ww`."""
        utterance = 'This ww good.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? good.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_x(self):
        """Test `x`."""
        utterance = 'x.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_repetition(self):
        """Test repetition."""
        utterance = 'test [x 2]'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'test [x 2]'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_x_part_of_word(self):
        """Test `x` being part of a word."""
        utterance = 'Regex'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'Regex'
        self.assertEqual(actual_output, desired_output)

    # clean_utterance

    def test_clean_utterance_mixed_things_to_clean(self):
        """Test all utterance cleaning methods at once.

        The utterance contains:
        - redundant whitespace
        - terminator
        - untranscribed
        - events
        - Null-event
        - repetition
        - scoped symbols
        - pause between words
        """
        utterance = ("+^ that's [x 2] xxx (..) mine ↓ &=vocalizes ; <0you"
                     " pig <she said   [=! cries]>> [=! slaps leg] +/.")
        actual_output = TurkishCleaner.clean_utterance(utterance)
        desired_output = "that's that's ??? mine pig she said"
        self.assertEqual(actual_output, desired_output)

    # clean_word

    def test_clean_word_mixed(self):
        """Test clean_word with markers, drawls, pauses and blocking."""
        actual_output = TurkishCleaner.clean_word('^ka:+l^e@e')
        desired_output = 'ka_le'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = '2S'
        actual = TurkishCleaner.clean_gloss(gloss)
        expected = '2SG'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'N:PROP'
        actual = TurkishCleaner.clean_pos(pos)
        expected = 'N'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'N:PROP'
        actual = TurkishCleaner.clean_pos_ud(pos_ud)
        expected = 'PROPN'
        self.assertEqual(actual, expected)