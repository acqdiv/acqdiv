import unittest

from acqdiv.parsers.corpora.main.japanese_miipro.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class TestJapaneseMiiProCleaner(unittest.TestCase):
    """Class to test the JapaneseMiiProCleaner."""

    cleaner = JapaneseMiiProCleaner()

    def test_remove_non_words_single(self):
        """Test remove_non_words with 1 non-word on the morphtier."""
        morph_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_multiple(self):
        """Test remove_non_words with 3 non-words on the morphtier."""
        morph_tier = 'tag|V n:prop|Ikun tag|do tag|‡ .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_no_non_words(self):
        """Test remove_non_words with no non-words on the morphtier."""
        morph_tier = 'n:prop|Ikun .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_empty_string(self):
        """Test remove_non_words with an empty string."""
        morph_tier = ''
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_single(self):
        """Test clean_morph_tier with 1 non-word and period."""
        morph_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_multiple(self):
        """Test clean_morph_tier with 3 non-words and question mark."""
        morph_tier = 'tag|da tag|do n:prop|Ikun tag|‡ ?'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_no_non_words(self):
        """Test clean_morph_tier with no non-words and excl mark."""
        morph_tier = 'n:prop|Ikun !'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_empty_string(self):
        """Test clean_morph_tier with no non-words and excl mark."""
        morph_tier = ''
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        """Test clean_seg_tier with 1 non-word.

        Since clean_seg_tier only calls clean_morph_tier and this method
        is already tested above, only one test to test the general
        functionality is used.
        """
        seg_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_seg_tier(seg_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier with 1 non-word.

        Since clean_gloss_tier only calls clean_morph_tier and this
        method is already tested above, only one test to test the
        general functionality is used.
        """
        gloss_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier with 1 non-word.

        Since clean_pos_tier only calls clean_morph_tier and this
        method is already tested above, only one test to test the
        general functionality is used.
        """
        pos_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_pos_tier(pos_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    # ---------- add_repetitions ----------

    def test_add_repetitions_aligned_no_scoping(self):
        raw_utterance = 'huhu repeat [x 2] hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_aligned_scoping(self):
        raw_utterance = 'huhu <ha ho> [x 2] hihi'
        morph_tier = 'N|huhu N|ha N|ho N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|ha N|ho N|ha N|ho N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_aligned_complicated_utt(self):
        raw_utterance = '+^ huhu [x 2] xxx [= not know] (..) ; haha [: höhö]'
        morph_tier = 'N|huhu N|xxx N|haha'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|huhu N|xxx N|haha'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_misaligned(self):
        raw_utterance = 'huhu repeat [x 2] hihi'
        morph_tier = 'N|huhu N|repeat N|hihi N|hö'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|repeat N|hihi N|hö'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_no_reps(self):
        raw_utterance = 'huhu haha hihi'
        morph_tier = 'N|huhu N|haha N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|haha N|hihi'
        self.assertEqual(actual_output, desired_output)

    # ---------- add retracings ----------

    def test_add_retracings_aligned_no_scoping(self):
        raw_utt = 'huhu repeat [/] repeat hihi'
        actual_utt = 'huhu repeat repeat hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_aligned_scoping(self):
        raw_utt = 'tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'tutu ha ho ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_misaligned1(self):
        raw_utt = 'tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'tutu ha ho ha ho kuku'
        morph_tier = 'N|bubu N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|bubu N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_misaligned2(self):
        raw_utt = 'bubu tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'bubu tutu ha ho ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_no_retracing(self):
        raw_utt = 'tutu ha ho kuku'
        actual_utt = 'tutu ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_unclean_actual_words(self):
        raw_utt = 'huhu repeat@o [/] repeat hihi'
        actual_utt = 'huhu repeat@o repeat hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = 'PRES'
        actual = JapaneseMiiProCleaner.clean_gloss(gloss)
        expected = 'PRS'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'sfx'
        actual = JapaneseMiiProCleaner.clean_pos(pos)
        expected = 'sfx'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'ptl:fina'
        actual = JapaneseMiiProCleaner.clean_pos_ud(pos_ud)
        expected = 'PART'
        self.assertEqual(actual, expected)
