import unittest

from acqdiv.parsers.corpora.main.nungon.cleaner import NungonCleaner


class TestNungonCleaner(unittest.TestCase):

    # ---------- remove_parentheses ----------

    def test_remove_parentheses(self):
        """Test remove_parentheses."""
        seg_tier = '(this is a test)'
        actual_output = NungonCleaner.remove_parentheses(seg_tier)
        desired_output = 'this is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_morph_tier ----------

    def test_clean_morph_tier(self):
        """Test clean_morph_tier."""
        morph_tier = 'PRON^this=is &=coughs ART^a N^test [laughs].'
        actual_output = NungonCleaner.clean_morph_tier(morph_tier)
        desired_output = 'PRON^this=is ART^a N^test'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_untranscribed(self):
        """Test clean_morph_tier with untranscribed morphology tier."""
        morph_tier = 'xxx'
        actual_output = NungonCleaner.clean_morph_tier(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_seg_tier ----------

    def test_clean_seg_tier(self):
        """Test clean_seg_tier."""
        morph_tier = 'this=is &=coughs (a) test [laughs].'
        actual_output = NungonCleaner.clean_seg_tier(morph_tier)
        desired_output = 'this=is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_untranscribed_morpheme_word ----------

    def test_unify_untranscribed_morpheme_word_single_question_mark(self):
        """Test unify_untranscribed_morpheme_word with single question mark."""
        word = '?'
        actual_output = NungonCleaner.unify_untranscribed_morpheme_word(word)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_morpheme_word_xxx(self):
        """Test unify_untranscribed_morpheme_word with xxx."""
        word = 'xxx'
        actual_output = NungonCleaner.unify_untranscribed_morpheme_word(word)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed_morph_tier ----------

    def test_null_untranscribed_morph_tier_single_question_mark(self):
        """Test null_untranscribed_morph_tier with single question mark."""
        utterance = '?'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_xxx(self):
        """Test null_untranscribed_morph_tier with xxx."""
        utterance = 'xxx'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_xxxx(self):
        """Test null_untranscribed_morph_tier with xxxx."""
        utterance = 'xxxx'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_with_angle_brackets(self):
        """Test null_untranscribed_morph_tier with <xxx>."""
        utterance = '<xxx>'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_question_mark ----------

    def test_remove_question_mark(self):
        """Test remove_question_mark."""
        morpheme = '?morpheme'
        actual_output = NungonCleaner.remove_question_mark(morpheme)
        desired_output = 'morpheme'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_trailing_hashtag ----------

    def test_remove_trailing_hashtag(self):
        """Test remove_trailing_hashtag."""
        word = 'pos^gloss#'
        actual_output = NungonCleaner.remove_trailing_hashtag(word)
        desired_output = 'pos^gloss'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_ambiguous_gloss_pos_word ----------

    def test_null_ambiguous_gloss_pos_word_two_variants(self):
        """Test null_ambiguous_gloss_pos_word with two variants."""
        word = 'N^mor-mor-mor#V^mor'
        actual_output = NungonCleaner.null_ambiguous_gloss_pos_word(word)
        desired_output = '???^???-???-???'
        self.assertEqual(actual_output, desired_output)

    def test_null_ambiguous_gloss_pos_word_three_variants(self):
        """Test null_ambiguous_gloss_pos_word with three variants."""
        word = 'N^mor-mor-mor#V^mor#P^mor-mor'
        actual_output = NungonCleaner.null_ambiguous_gloss_pos_word(word)
        desired_output = '???^???-???-???'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = '1sg.poss'
        actual = NungonCleaner.clean_gloss(gloss)
        expected = '1SG.POSS'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'v'
        actual = NungonCleaner.clean_pos(pos)
        expected = 'V'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'v'
        actual = NungonCleaner.clean_pos_ud(pos_ud)
        expected = 'VERB'
        self.assertEqual(actual, expected)