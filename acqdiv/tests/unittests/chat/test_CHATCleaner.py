import unittest
from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import BaseCHATCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    Class to test the BaseCHATCleaner.

    A lot of the test cases are taken from or inspired by
    https://talkbank.org/manuals/CHAT.pdf
    .
    """

    # ---------- metadata cleaning ----------

    def test_clean_date_regular_date(self):
        """Test clean_date with a regular date as input."""
        actual_output = BaseCHATCleaner.clean_date('12-SEP-1997')
        desired_output = '1997-09-12'
        self.assertEqual(actual_output, desired_output)

    def test_clean_date_empty_string(self):
        """Test clean_date with empty string as input."""
        actual_output = BaseCHATCleaner.clean_date('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test utterance cleaning ----------

    # Tests for the clean_utterance-method.

    def test_clean_utterance_clean_utt(self):
        """Test remove utterance using with already clean utterance."""
        utterance = "that's mine she said"
        actual_output = BaseCHATCleaner.clean_utterance(utterance)
        desired_output = "that's mine she said"
        self.assertEqual(actual_output, desired_output)

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
        actual_output = BaseCHATCleaner.clean_utterance(utterance)
        desired_output = "that's that's ??? mine pig she said"
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        """Test clean_utterance with an empty string."""
        utterance = ''
        actual_output = BaseCHATCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_null(self):
        """Test with null utterance."""
        utterance = '0[=! applauses]'
        actual_output = BaseCHATCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test word cleaning ----------

    def test_remove_form_markers_empty_string(self):
        """Test remove_form_markers with empty string."""
        actual_output = BaseCHATCleaner.remove_form_markers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_form_markers-method.

    def test_remove_form_markers_l_marked_one_char_length(self):
        """Test remove_form_markers with marks of one char length."""
        word = 'mark@l'
        actual_output = BaseCHATCleaner.remove_form_markers(
            word)
        desired_output = "mark"
        self.assertEqual(actual_output, desired_output)

    def test_remove_form_markers_si_marked_two_char_length(self):
        """Test remove_form_markers with mark of two chars length."""
        actual_output = BaseCHATCleaner.remove_form_markers(
            'mark@si')
        desired_output = 'mark'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_form_markers_mixed_'
                    'no_space_before_terminator skipping'))
    def test_remove_form_markers_mixed_no_space_before_terminator(self):
        """Test remove_form_markers with 1 '@k' and one '@l' mark.

        No space between mark and terminator.
        """
        actual_output = BaseCHATCleaner.remove_form_markers(
            "mark@k.")
        desired_output = "mark."
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_drawls-method.

    def test_remove_drawls_single_lengthened_syllable(self):
        """Test remove_drawls with 1 lengthened syllable (:)."""
        actual_output = BaseCHATCleaner.remove_drawls('bana:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_multiple_lengthened_syllables(self):
        """Test remove_drawls with 2 lengthened syllables (:)."""
        actual_output = BaseCHATCleaner.remove_drawls('ba:na:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_empty_string(self):
        """Test remove_drawls with an empty string."""
        actual_output = BaseCHATCleaner.remove_drawls('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_pauses_within_words-method.

    def test_remove_pauses_within_words_one_pause(self):
        """Test remove_pauses with 1 pause (^)."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words(
            'spa^ghetti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_multiple_pauses(self):
        """Test remove_pauses with 2 pauses (^)."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words(
            'spa^ghe^tti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_two_pauses_one_letter_in_between(self):
        """Test remove_pauses with two pauses separated by one letter."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words('m^a^t')
        desired_output = 'mat'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_pause_at_the_end(self):
        """Test remove_pauses with one pause at the end."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words('ma^')
        desired_output = 'ma'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_blocking(self):
        """Test remove_pauses with blocking."""
        actual_output = BaseCHATCleaner.remove_pauses_within_words('^hey')
        desired_output = '^hey'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_blocking-method. (≠ or ^)

    def test_remove_blocking_unequal_sign(self):
        """Test remove_blocking with an unequal sign as marker (≠)."""
        actual_output = BaseCHATCleaner.remove_blocking(
            '≠hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_circumflex(self):
        """Test remove_blocking with a circumflex as marker (^)."""
        actual_output = BaseCHATCleaner.remove_blocking(
            '^there')
        desired_output = 'there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_empty_string(self):
        """Test remove_blocking with an empty string."""
        actual_output = BaseCHATCleaner.remove_blocking('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_fillers-method.

    def test_remove_filler_without_dash(self):
        """Test remove_filler without dash."""
        word = '&hu'
        actual_output = BaseCHATCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_with_dash(self):
        """Test remove_fillers with dash."""
        word = '&-hu'
        actual_output = BaseCHATCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_empty_string(self):
        """Test remove_fillers with 3 fillers (&-uh)."""
        word = ''
        actual_output = BaseCHATCleaner.remove_filler(word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_ampersand_with_equal_sign(self):
        """Test remove_fillers with ampersand and equal sign."""
        word = '&=hu'
        actual_output = BaseCHATCleaner.remove_filler(word)
        desired_output = '&=hu'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_already_clean(self):
        """Test clean_word with an already clean word."""
        actual_output = BaseCHATCleaner.clean_word('ka')
        desired_output = 'ka'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_mixed(self):
        """Test clean_word with markers, drawls, pauses and blocking."""
        actual_output = BaseCHATCleaner.clean_word('^ka:l^e@e')
        desired_output = 'kale'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_empty_string(self):
        """Test clean_word with an empty string."""
        actual_output = BaseCHATCleaner.clean_word('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test morphology tier cleaning ----------

    def test_clean_seg_tier(self):
        """Test clean_seg_tier for same input as output."""
        seg_tier = 'ha be'
        actual_output = BaseCHATCleaner.clean_seg_tier(seg_tier)
        desired_output = seg_tier
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier for same input as output."""
        gloss_tier = 'ha be'
        actual_output = BaseCHATCleaner.clean_gloss_tier(gloss_tier)
        desired_output = gloss_tier
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier for same input as output."""
        pos_tier = 'ha be'
        actual_output = BaseCHATCleaner.clean_pos_tier(pos_tier)
        desired_output = pos_tier
        self.assertEqual(actual_output, desired_output)

    # ---------- cross cleaning ---------

    def test_utterance_cross_clean(self):
        """Test utterance_cross_clean for same input as output."""
        raw_utt = ''
        actual_utt = 'ha be'
        target_utt = 'ha be'
        seg_tier = 'h_a b_e'
        gloss_tier = '1sg pl'
        pos_tier = 'V N'
        actual_output = BaseCHATCleaner.utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier)
        desired_output = (actual_utt, target_utt, seg_tier, gloss_tier,
                          pos_tier)
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme word cleaning ----------

    def test_clean_seg_word(self):
        """Test clean_seg_word, same input as output."""
        seg_word = 'ke'
        actual_output = BaseCHATCleaner.clean_seg_word(seg_word)
        desired_output = seg_word
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_word(self):
        """Test clean_gloss_word, same input as output."""
        gloss_word = 'wh'
        actual_output = BaseCHATCleaner.clean_gloss_word(gloss_word)
        desired_output = gloss_word
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_word(self):
        """Test clean_pos_word, same input as output."""
        pos_word = 'V'
        actual_output = BaseCHATCleaner.clean_pos_word(pos_word)
        desired_output = pos_word
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme cleaning ----------

    def test_clean_segment(self):
        """Test clean_segment, same input as output."""
        segment = 'he'
        actual_output = BaseCHATCleaner.clean_segment(segment)
        desired_output = segment
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        """Test clean_gloss, same input as output."""
        gloss = 'he'
        actual_output = BaseCHATCleaner.clean_gloss(gloss)
        desired_output = gloss
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos(self):
        """Test clean_pos, same input as output."""
        pos = 'he'
        actual_output = BaseCHATCleaner.clean_pos(pos)
        desired_output = pos
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
