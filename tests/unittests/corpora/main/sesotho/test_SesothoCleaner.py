import unittest

from acqdiv.parsers.corpora.main.sesotho.cleaner import SesothoCleaner


class TestSesothoCleaner(unittest.TestCase):

    # ---------- utterance cleaning ----------

    def test_clean_utterance_parenthesized_words(self):
        """Test clean_utterance with parenthesized words.

        Two words entirely surrounded by parentheses and two words
        partly surrounded by parentheses.
        """
        utterance = '(ho)dula tsamaya  (ho)dula (uye) ausi (uye) .'
        actual_output = SesothoCleaner.clean_utterance(utterance)
        desired_output = 'hodula tsamaya hodula ausi'
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        """Test clean_utterance with empty string."""
        utterance = ''
        actual_output = SesothoCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_single_beginning(self):
        """Test remove_words_parentheses with 1 parenth. word at beginning."""
        utterance = '(uye) ausi .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_single_end(self):
        """Test remove_words_parentheses with 1 parenth. word at end."""
        utterance = 'ausi (uye) .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_multiple(self):
        """Test remove_words_parentheses with 3 word in parentheses."""
        utterance = '(uye) ausi (uye) (uye) .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_empty_string(self):
        """Test remove_words_parentheses with an empty string."""
        utterance = ''
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_single(self):
        """Test remove_parentheses with 1 word partly surrounded."""
        utterance = '(ho)dula pela ausi Mamello .'
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = 'hodula pela ausi Mamello .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_multiple(self):
        """Test remove_parentheses with 3 words partly surrounded."""
        utterance = '(ho)dula pela (ho)dula (ho)dula .'
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = 'hodula pela hodula hodula .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_empty_string(self):
        """Test remove_parentheses with an empty string"""
        utterance = ''
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_translation(self):
        """Test clean_translation with a timestamp."""
        translation = 'I ate it 502058_507330'
        actual_output = SesothoCleaner.clean_translation(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_with_timestamp(self):
        """Test remove_timestamp with a timestamp."""
        translation = 'I ate it 502058_507330'
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_no_timestamp(self):
        """Test remove_timestamp with no timestamp."""
        translation = 'I ate it'
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_empty_string(self):
        """Test remove_timestamp with an empty string."""
        translation = ''
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- cross cleaning ----------

    def test_remove_contractions_single(self):
        """Test remove contractions with one contraction."""
        seg_tier = 'e tsamay-a (u-y-e) (ho-)dul-a pela ausi Mamello .'
        gloss_tier = ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in loc '
                      'sister(1a , 2a) n^name .')
        pos_tier = ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in loc '
                    'sister(1a , 2a) n^name .')
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = 'e tsamay-a (ho-)dul-a pela ausi Mamello .'
        gloss_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                          'n^name .')
        pos_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                        'n^name .')
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    def test_remove_contractions_multiple(self):
        """Test remove contractions with three contractions."""
        seg_tier = ('(u-y-e) e tsamay-a (u-y-e) (ho-)dul-a pela ausi Mamello '
                    '(u-y-e) .')
        gloss_tier = ('(sm2s-t^p_v^go-m^s) ij v^leave-m^i (sm2s-t^p_v^go-m^s) '
                      '(if-)v^sit-m^in loc sister(1a , 2a) n^name '
                      '(sm2s-t^p_v^go-m^s) .')
        pos_tier = ('(sm2s-t^p_v^go-m^s) ij v^leave-m^i (sm2s-t^p_v^go-m^s) '
                    '(if-)v^sit-m^in loc sister(1a , 2a) n^name '
                    '(sm2s-t^p_v^go-m^s) .')
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = 'e tsamay-a (ho-)dul-a pela ausi Mamello .'
        gloss_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                          'n^name .')
        pos_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                        'n^name .')
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    def test_remove_contractions_empty_string(self):
        """Test remove contractions with an empty string."""
        seg_tier = ''
        gloss_tier = ''
        pos_tier = ''
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = ''
        gloss_tier_des = ''
        pos_tier_des = ''
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    # ---------- test morpheme cleaning ----------

    def test_clean_seg_tier(self):
        """Test clean_seg tier with terminator."""
        seg_tier = 'm-ph-e ntho .'
        actual_output = SesothoCleaner.clean_seg_tier(seg_tier)
        desired_output = 'm-ph-e ntho'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier_empty_string(self):
        """Test clean_seg tier with empty string."""
        seg_tier = ''
        actual_output = SesothoCleaner.clean_seg_tier(seg_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier_standard_case(self):
        """Test clean_gloss_tier.

        Test for noun class spaces, noun class separators and
        terminators.
        """
        gloss_tier = 'n^10-bucket(9 , 10/6) ?'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier_empty_string(self):
        """Test clean_gloss_tier with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_spaces_noun_class_parentheses_standard_case(self):
        """Test remove_spaces_noun_class_parentheses."""
        gloss_tier = 'n^10-bucket(9 , 10) ?'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10)'
        self.assertEqual(actual_output, desired_output)

    def test_remove_spaces_noun_class_parentheses_empty_string(self):
        """Test remove_spaces_noun_class_parentheses with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_replace_noun_class_separator_standard_case(self):
        """Test replace_noun_class_separator with one separator."""
        gloss_tier = 'n^10-bucket(9 , 10/6)'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_replace_noun_class_separator_empty_string(self):
        """Test replace_noun_class_separator with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier_standart_case(self):
        """Test clean_pos_tier with a noun class and separator.

        Should behave the same as clean_gloss_tier.
        """
        pos_tier = 'n^10-bucket(9 , 10/6) ?'
        actual_output = SesothoCleaner.clean_pos_tier(pos_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier_empty_string(self):
        """Test clean_pos_tier with an empty string.

        Should behave the same as clean_gloss_tier.
        """
        pos_tier = ''
        actual_output = SesothoCleaner.clean_pos_tier(pos_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word_one_pair_parentheses(self):
        """Test clean_seg_word with one pair of parentheses."""
        seg_word = '(ho)nada'
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word_two_pairs_parentheses(self):
        """Test clean_seg_word with two pairs of parentheses."""
        seg_word = '(ho)nad(a)'
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word_empty_string(self):
        """Test clean_seg_word with an empty string."""
        seg_word = ''
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_one_concatenator(self):
        """Test replace_concatenators with one concatenator."""
        gloss_word = 'sm2s-t^p_om1s-v^touch-m^in'
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = 'sm2s-t^p.om1s-v^touch-m^in'
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_multiple_concatenators(self):
        """Test replace_concatenators with three concatenators.

        But only one of them should be replaced by a dot. The others are
        verb-multi-word-expressions.

        Note: Not clear if middle '_' should be replaced.
        """
        gloss_word = 'sm2s-t^p_om1s-v^touch-m^in_v^go_out'
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = 'sm2s-t^p.om1s-v^touch-m^in_v^go_out'
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_empty_string(self):
        """Test replace_concatenators with an empty string."""
        gloss_word = ''
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_inf_standard_case(self):
        """Test remove_parentheses_inf with one pair of parentheses."""
        gloss_word = '(ho)nada'
        actual_output = SesothoCleaner.remove_parentheses(gloss_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_inf_empty_string(self):
        """Test remove_parentheses_inf with an empty string."""
        gloss_word = '(ho)nada'
        actual_output = SesothoCleaner.remove_parentheses(gloss_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = 'sm2s'
        actual = SesothoCleaner.clean_gloss(gloss)
        expected = '2SG.SBJ'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'd'
        actual = SesothoCleaner.clean_pos(pos)
        expected = 'PRODEM'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'd'
        actual = SesothoCleaner.clean_pos_ud(pos_ud)
        expected = 'PRON'
        self.assertEqual(actual, expected)