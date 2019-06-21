import unittest

from acqdiv.parsers.corpora.main.cree.CreeCleaner import CreeCleaner


class TestCreeCleaner(unittest.TestCase):
    """Class to test the Cree cleaner"""

    # ---------- utterance cleaning ----------

    # Tests for the remove_angle_brackets-method.

    def test_remove_angle_brackets_standard_case(self):
        """Test remove_angle_brackets with standard angle brack case."""
        input_str = '‹mâ ehtad-g› .'
        actual_output = CreeCleaner.remove_angle_brackets(input_str)
        desired_output = 'mâ ehtad-g .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_angle_brackets_empty_string(self):
        """Test remove_angle_brackets with an empty string."""
        actual_output = CreeCleaner.remove_angle_brackets('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_mixed(self):
        """Test clean_utterance with angle brackets and scoped symbols."""
        utterance = '‹hey there [=! cries]›'
        actual_output = CreeCleaner.clean_utterance(utterance)
        desired_output = 'hey there'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_morpheme_separators-method.

    def test_remove_morpheme_separators_single_separator(self):
        """Test remove_morpheme_separators with 1 separator (_)."""
        input_str = 'bye_bye'
        actual_output = CreeCleaner.remove_morph_separators(input_str)
        desired_output = 'byebye'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morpheme_separators_multiple_separators(self):
        """Test remove_morpheme_separators with 2 separators (_)."""
        input_str = 'ha_ha_train'
        actual_output = CreeCleaner.remove_morph_separators(input_str)
        desired_output = 'hahatrain'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morpheme_separators_empty_string(self):
        """Test remove_morpheme_separators with an empty string."""
        actual_output = CreeCleaner.remove_morph_separators('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_already_clean(self):
        """Test clean word with a already clean word."""
        actual_output = CreeCleaner.clean_word('ke')
        desired_output = 'ke'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_already_mixed(self):
        """Test clean_word with Cases Cree-specific and non-Cree-specific.

        Cases:
        - zero-morpheme
        - morph-separator
        - blocking
        - drawls
        """
        actual_output = CreeCleaner.clean_word('^ke_ke:na-zéro')
        desired_output = 'kekena-Ø'
        self.assertEqual(actual_output, desired_output)

    # ---------- morphology tier cleaning ----------

    # Test for the replace_zero-method.

    def test_replace_zero_single_zero(self):
        """Test replace_zero with 1 zero (zéro)."""
        input_str = 'puhchu~shum~zéro'
        actual_output = CreeCleaner.replace_zero(input_str)
        desired_output = 'puhchu~shum~Ø'
        self.assertEqual(actual_output, desired_output)

    def test_replace_zero_multiple_zeros(self):
        """Test replace_zero with 3 zeros (zéro)."""
        input_str = 'zéro~ʤʊ~zéro~zéro'
        actual_output = CreeCleaner.replace_zero(input_str)
        desired_output = 'Ø~ʤʊ~Ø~Ø'
        self.assertEqual(actual_output, desired_output)

    def test_replace_zero_empty_string(self):
        """Test replace_zero with an empty string."""
        actual_output = CreeCleaner.replace_zero('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_morpheme_separator-method.

    def test_replace_morpheme_separator_single_separator(self):
        """Test replace_morpheme_separator with 1 separator."""
        input_str = 'puhchu~shun'
        actual_output = CreeCleaner.replace_morpheme_separator(input_str)
        desired_output = 'puhchushun'
        self.assertEqual(actual_output, desired_output)

    def test_replace_morpheme_separator_multiple_separators(self):
        """Test replace_morpheme_separator with 2 separators."""
        input_str = 'puhchu~sum~zéro'
        actual_output = CreeCleaner.replace_morpheme_separator(input_str)
        desired_output = 'puhchusumzéro'
        self.assertEqual(actual_output, desired_output)

    def test_replace_morpheme_separator_empty_string(self):
        """Test replace_morpheme_separator with an empty string."""
        actual_output = CreeCleaner.replace_morpheme_separator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_square_brackets-method.
    # Nested brackets or multiple bracket pairs on the same line
    # are not present in the corpus and thus not tested for.

    def test_remove_square_brackets_standard_case(self):
        """Test remove_square_brackets with normal case ([...])."""
        input_str = '[ɡaɡa nɛɹa nena mətɑ]'
        actual_output = CreeCleaner.remove_square_brackets(input_str)
        desired_output = 'ɡaɡa nɛɹa nena mətɑ'
        self.assertEqual(actual_output, desired_output)

    def test_remove_square_brackets_empty_string(self):
        """Test remove_square_brackets with empty string."""
        actual_output = CreeCleaner.remove_square_brackets('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_untranscribed_morph_tier-method.

    def test_null_untranscribed_morph_tier_method_standard_case(self):
        """Test null_untranscribed_morph_tier with standard case (*)."""
        actual_output = CreeCleaner.null_untranscribed_morph_tier('*')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_method_empty_string(self):
        """Test null_untranscribed_morph_tier with empty string."""
        actual_output = CreeCleaner.null_untranscribed_morph_tier('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_mixed(self):
        """Test clean_morph_tier with square brackets and untranscribed."""
        actual_output = CreeCleaner.clean_morph_tier('[*]')
        desired_output = '*'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_empty_string(self):
        """Test clean_morph_tier with an empty string."""
        actual_output = CreeCleaner.clean_morph_tier('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        """Test clean_seg_tier."""
        seg_tier = '[1~initial~vta.fin~passive~zzz]'
        actual_output = CreeCleaner.clean_seg_tier(seg_tier)
        desired_output = '1~initial~vta.fin~passive~zzz'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier."""
        gloss_tier = '[1~initial~vta.fin~passive~zzz]'
        actual_output = CreeCleaner.clean_gloss_tier(gloss_tier)
        desired_output = '1~initial~vta.fin~passive~zzz'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier."""
        pos_tier = '[1~initial~vta.fin~passive~zzz]'
        actual_output = CreeCleaner.clean_pos_tier(pos_tier)
        desired_output = '1~initial~vta.fin~passive~zzz'
        self.assertEqual(actual_output, desired_output)

    # ---------- cross cleaning ----------

    # Tests for the replace_eng-method.

    def test_replace_eng_single_eng(self):
        """Test replace_eng with 1 Eng to be replaced."""
        gloss_tier = 'Eng'
        utterance = 'floor'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'floor'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_multiple_engs(self):
        """Test replace_eng with 4 Engs to be replaced."""
        gloss_tier = 'remove~by. emph Eng Eng Eng Eng'
        utterance = 'min~in~ikiniu~h wâsh these are taken off'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'remove~by. emph these are taken off'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_at_beginning_end(self):
        """Test replace_eng with Engs at the start/end of the gloss."""
        gloss_tier = 'Eng fin~3.sg Eng'
        utterance = 'garbage â~u garbage'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'garbage fin~3.sg garbage'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_tiers_misaligned(self):
        """Test replace_eng with word tier longer than gloss tier.

        Since tiers are of unequal length, return the gloss tier
        unchanged.
        """
        gloss_tier = 'Eng fin~3.sg'
        utterance = 'garbage â~u garbage'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'Eng fin~3.sg'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_emtpy_string(self):
        """Test replace_eng with an empty string."""
        actual_output = CreeCleaner.replace_eng('', '')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_utterance_cross_clean(self):
        """Test utterance_cross_clean with several engs."""
        raw_utt = ''
        actual_utt = 'hi ha be bye'
        target_utt = 'hi ha be bye'
        seg_tier = 'ke h_a b_e me'
        gloss_tier = 'Eng 1sg pl Eng'
        pos_tier = 'N V N V'
        actual_output = CreeCleaner.utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier)
        desired_output = (actual_utt, target_utt, seg_tier, 'hi 1sg pl bye',
                          pos_tier)
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_percentages-method.

    def test_replace_percentages_untranscribed_word(self):
        """Test replace_percentages with an untranscribed word (%%%)."""
        actual_output = CreeCleaner.replace_percentages('%%%')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_percentages_normal_word(self):
        """Test replace_percentages with a normal word."""
        actual_output = CreeCleaner.replace_percentages('hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_replace_percentages_empty_string(self):
        """Test replace_percentages with en empty string."""
        actual_output = CreeCleaner.replace_percentages('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_hashtag-method.

    def test_replace_hashtag_unglossed_word(self):
        """Test replace_hashtag with an unglossed word (%%%)."""
        actual_output = CreeCleaner.replace_hashtag('#')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_hashtag_normal_word(self):
        """Test replace_hashtag with a normal word."""
        actual_output = CreeCleaner.replace_hashtag('hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_replace_hashtag_empty_string(self):
        """Test replace_hashtag with an empty string."""
        actual_output = CreeCleaner.replace_hashtag('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the handle_question_mark-method.

    def test_handle_question_mark_single_question_mark(self):
        """Test handle_question_mark with single question mark."""
        actual_output = CreeCleaner.handle_question_mark('?')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_handle_question_mark_question_mark_at_the_end(self):
        """Test handle_question_mark question mark at end of morph."""
        actual_output = CreeCleaner.handle_question_mark('dok?')
        desired_output = 'dok'
        self.assertEqual(actual_output, desired_output)

    def test_handle_question_mark_empty_string(self):
        """Test handle_question_mark with an empty string."""
        actual_output = CreeCleaner.handle_question_mark('dok?')
        desired_output = 'dok'
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_star-method.

    def test_replace_star_case_star(self):
        """Test handle_question_mark with a star."""
        actual_output = CreeCleaner.replace_star('*')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_star_non_star_morpheme(self):
        """Test handle_question_mark with a non star morpheme."""
        actual_output = CreeCleaner.replace_star('muw~du')
        desired_output = 'muw~du'
        self.assertEqual(actual_output, desired_output)

    def test_replace_star_empty_string(self):
        """Test handle_question_mark with an empty string."""
        actual_output = CreeCleaner.replace_star('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for replace_gloss_connector.

    def replace_gloss_connector_multiple_plus_and_comma(self):
        """Test replace_gloss_connector with 2 commas and 2 pluses."""
        gloss = 'a,quest sm+gur2 a,quest sm+gur2'
        actual_output = CreeCleaner.replace_gloss_connector(gloss)
        desired_output = 'a.quest sm.gur2 a.quest sm.gur2'
        self.assertEqual(actual_output, desired_output)

    def replace_gloss_connector_empty_string(self):
        """Test replace_gloss_connector with empty string."""
        actual_output = CreeCleaner.replace_gloss_connector('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the uppercase_pos_in_parentheses-method.

    def test_uppercase_pos_in_parentheses_one_parenth_pair(self):
        """Test uppercase_pos_in_parentheses with one pair."""
        pos = 'na eˈp~o~(h)'
        actual_output = CreeCleaner.uppercase_pos_in_parentheses(pos)
        desired_output = 'na eˈp~o~(H)'
        self.assertEqual(actual_output, desired_output)

    def test_uppercase_pos_in_parentheses_empty_string(self):
        """Test uppercase_pos_in_parentheses with empty string."""
        actual_output = CreeCleaner.uppercase_pos_in_parentheses('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)