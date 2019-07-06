import unittest

from acqdiv.parsers.chat.readers.ActualTargetUtteranceExtractor \
    import ActualTargetUtteranceExtractor as Extractor


class TestActualTargetUtteranceExtractor(unittest.TestCase):

    # Test for the get_shortening_actual-method.

    def test_get_shortening_actual_standard_case(self):
        """Test get_shortening_actual with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'na:da <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_multiple_shortenings(self):
        """Test get_shortening_actual with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'na:da dükäm lan [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_non_shortening_parentheses(self):
        """Test get_shortening_actual with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'mo:da (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_special_characters(self):
        """Test get_shortening_actual with special chars in parentheses."""
        utterance = 'Tu:(ğ)çe .'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_no_shortening(self):
        """Test get_shortening_actual using utt without shortening."""
        utterance = 'Tu:çe .'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_empty_string(self):
        """Test get_shortening_actual with an empty string."""
        utterance = 'Tu:çe .'
        actual_output = Extractor.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    # Test for the get_shortening_target-method.

    def test_get_shortening_target_standard_case(self):
        """Test get_shortening_target with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = 'na:rada <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_multiple_shortenings(self):
        """Test get_shortening_target with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = 'ona:rada dükäm landa [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_non_shortening_parentheses(self):
        """Test get_shortening_target with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = 'mo:rada (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_special_characters(self):
        """Test get_shortening_target with special chars in parentheses."""
        utterance = 'Mu:(ğ)ça .'
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = 'Mu:ğça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_no_shortening(self):
        """Test get_shortening_target using utt without a shortening."""
        utterance = 'Mu:ça .'
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = 'Mu:ça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_empty_string(self):
        """Test get_shortening_target with an empty string."""
        utterance = ''
        actual_output = Extractor.get_shortening_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_actual-method.

    def test_get_replacement_actual_one_replacement(self):
        """Test get_replacement_actual with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = Extractor.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_multiple_replacements(self):
        """Test get_replacement_actual with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = Extractor.get_replacement_actual(utterance)
        desired_output = 'yarasam yarasam yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_no_replacement(self):
        """Test get_replacement_actual with no replacement."""
        utterance = 'yarasam .'
        actual_output = Extractor.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_empty_string(self):
        """Test get_replacement_actual with an empty string."""
        utterance = ''
        actual_output = Extractor.get_replacement_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_no_whitespace(self):
        """Test get_replacement_actual with missing whitespace."""
        utterance = 'shoulda[: should have]'
        actual_output = Extractor.get_replacement_actual(utterance)
        desired_output = 'shoulda'
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_target-method.

    def test_get_replacement_target_one_replacement(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_multiple_replacements(self):
        """Test get_replacement_target with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'yorosom yorosom yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_no_replacement(self):
        """Test get_replacement_target with no replacement."""
        utterance = 'yarasam .'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_empty_string(self):
        """Test get_replacement_target with an empty string."""
        utterance = ''
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_one_by_two(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'shoulda [: should have]'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'should_have'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_one_by_three(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'shouldada [: should have done]'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'should_have_done'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_no_withespace(self):
        """Test without whitespace."""
        utterance = 'shouldada[: should have done]'
        actual_output = Extractor.get_replacement_target(utterance)
        desired_output = 'should_have_done'
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_actual-method.

    def test_get_fragment_actual_one_fragment(self):
        """Test get_fragment_actual with 1 fragment."""
        utterance = '&ab .'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = 'ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_multiple_fragments(self):
        """Test get_fragment_actual with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = 'ab a ab b ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_no_fragments(self):
        """Test get_fragment_actual using an utt without fragments."""
        utterance = 'a b .'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_empty_string(self):
        """Test get_fragment_actual with an empty string."""
        utterance = ''
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_ampersand_outside(self):
        """Test get_fragment_actual with ampersand outside fragment."""
        utterance = '&=laugh &wow &-um'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = '&=laugh wow &-um'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_one_char_fragment(self):
        """Test with a fragment consisting of one character."""
        utterance = 'This is &a test'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = 'This is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_ampersand_inside_word(self):
        """Test with ampersand occurring inside the word."""
        utterance = 'dont&delete'
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = 'dont&delete'
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_target-method.

    def test_get_fragment_target_one_fragment(self):
        """Test get_fragment_target with 1 fragment."""
        utterance = '&ab .'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = 'xxx .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_multiple_fragments(self):
        """Test get_fragment_target with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = 'xxx a xxx b xxx .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_no_fragments(self):
        """Test get_fragment_target using an utt without fragments."""
        utterance = 'a b .'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_empty_string(self):
        """Test get_fragment_target with an empty string."""
        utterance = ''
        actual_output = Extractor.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_ampersand_outside(self):
        """Test get_fragment_target with ampersand outside fragment."""
        utterance = '&=laugh &wow &-um'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = '&=laugh xxx &-um'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_one_char_fragment(self):
        """Test with a fragment consisting of one character."""
        utterance = 'This is &a test'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = 'This is xxx test'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_ampersand_inside_word(self):
        """Test with ampersand occurring inside the word."""
        utterance = 'dont&handle'
        actual_output = Extractor.get_fragment_target(utterance)
        desired_output = 'dont&handle'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_retracing_actual ----------

    def test_get_retracing_actual_retracing(self):
        """Test get_retracing_actual."""
        utterance = 'this is [/] is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_retracing_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<this is> [/] this is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this is this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_correction(self):
        """Test get_retracing_actual."""
        utterance = 'this us [//] is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this us is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_correction_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<this us> [//] this is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this us this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_reformulation(self):
        """Test get_retracing_actual."""
        utterance = 'what [///] why do you eat'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_reformulation_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<for what> [///] why do you eat'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'for what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_false_start(self):
        """Test get_retracing_actual."""
        utterance = 'I want [/-] would do that'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'I want would do that'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_false_start_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<I want> [///] what do you eat'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'I want what do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_no_whitespace(self):
        """Test with missing whitespace."""
        utterance = 'this is[/] is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_retracing_several_words_no_whitespace(self):
        """Test retracing with several words and missing whitespace."""
        utterance = '<this is>[/] this is a test'
        actual_output = Extractor.get_retracing_actual(utterance)
        desired_output = 'this is this is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_retracing_target ----------

    def test_get_retracing_target_retracing(self):
        """Test get_retracing_target."""
        utterance = 'this is [/] is a test'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_retracing_several_words(self):
        """Test get_retracing_target."""
        utterance = '<this is> [/] this is a test'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'this is this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_correction(self):
        """Test get_retracing_target."""
        utterance = 'this us [//] is a test'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_correction_several_words(self):
        """Test get_retracing_target."""
        utterance = '<this us> [//] this is a test'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'this us this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_reformulation(self):
        """Test get_retracing_target."""
        utterance = 'what [///] why do you eat'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_reformulation_several_words(self):
        """Test get_retracing_target."""
        utterance = '<for what> [///] why do you eat'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'for what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_false_start(self):
        """Test get_retracing_target."""
        utterance = 'I want [/-] would do that'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'I want would do that'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_false_start_several_words(self):
        """Test get_retracing_target."""
        utterance = '<I want> [///] what do you eat'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'I want what do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_correction_no_whitespace(self):
        """Test with correction and missing whitespace."""
        utterance = 'this us[//] is a test'
        actual_output = Extractor.get_retracing_target(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- to_actual_utterance ----------

    def test_to_actual_utterance_empty_string(self):
        utterance = ''
        actual_output = Extractor.to_actual_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_no_occurrences(self):
        """Test get_actual_utterance using an utt without occurrences."""
        utterance = 'mu:ça yarasam ab yarasam ac'
        actual_output = Extractor.to_actual_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_one_occurence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        utterance = 'Mu:(ğ)ça &ab yarasam [: yorosom]'
        actual_output = Extractor.to_actual_utterance(utterance)
        desired_output = 'Mu:ça ab yarasam'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_multiple_occurences_of_each(self):
        """Test with 2 shortenings, 2 fragments and 2 replacements."""
        utterance = ('(A)mu:(ğ)ça yarasam [: yorosom] '
                     '&ab yarasam [: yorosom] &ac')
        actual_output = Extractor.to_actual_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_nesting(self):
        """Test with nesting."""
        utterance = '<it shoulda[: should have]> [<2] ?'
        actual_output = Extractor.to_actual_utterance(utterance)
        desired_output = '<it shoulda> [<2] ?'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_empty_string(self):
        utterance = ''
        actual_output = Extractor.to_target_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_no_occurrences(self):
        """Test to_target_utterance using an utterance without occurrences."""
        utterance = 'mu:ça yarasam ab yarasam ac'
        actual_output = Extractor.to_target_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_one_occurrence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        utterance = 'Mu:(ğ)ça &ab yarasam [: yorosom]'
        actual_output = Extractor.to_target_utterance(utterance)
        desired_output = 'Mu:ğça xxx yorosom'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_multiple_occurrences_of_each(self):
        """Test with 2 shortenings, 2 fragments and 2 replacements."""
        utterance = ('yarasam [: yorosom] '
                     '&ab (a)mu:(ğ)ça  &ac yarasam [: yorosom]')
        actual_output = Extractor.to_target_utterance(utterance)
        desired_output = 'yorosom xxx amu:ğça  xxx yorosom'
        self.assertEqual(actual_output, desired_output)
