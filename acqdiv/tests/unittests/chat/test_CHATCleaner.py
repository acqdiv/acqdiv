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
