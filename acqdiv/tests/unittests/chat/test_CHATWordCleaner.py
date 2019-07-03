import unittest
from acqdiv.parsers.chat.cleaners.CHATWordCleaner import CHATWordCleaner


class TestCHATWordCleaner(unittest.TestCase):
    
    def test_remove_form_markers_empty_string(self):
        """Test remove_form_markers with empty string."""
        actual_output = CHATWordCleaner.remove_form_markers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_form_markers-method.

    def test_remove_form_markers_l_marked_one_char_length(self):
        """Test remove_form_markers with marks of one char length."""
        word = 'mark@l'
        actual_output = CHATWordCleaner.remove_form_markers(
            word)
        desired_output = "mark"
        self.assertEqual(actual_output, desired_output)

    def test_remove_form_markers_si_marked_two_char_length(self):
        """Test remove_form_markers with mark of two chars length."""
        actual_output = CHATWordCleaner.remove_form_markers(
            'mark@si')
        desired_output = 'mark'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_form_markers_mixed_'
                    'no_space_before_terminator skipping'))
    def test_remove_form_markers_mixed_no_space_before_terminator(self):
        """Test remove_form_markers with 1 '@k' and one '@l' mark.

        No space between mark and terminator.
        """
        actual_output = CHATWordCleaner.remove_form_markers(
            "mark@k.")
        desired_output = "mark."
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_drawls-method.

    def test_remove_drawls_single_lengthened_syllable(self):
        """Test remove_drawls with 1 lengthened syllable (:)."""
        actual_output = CHATWordCleaner.remove_drawls('bana:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_multiple_lengthened_syllables(self):
        """Test remove_drawls with 2 lengthened syllables (:)."""
        actual_output = CHATWordCleaner.remove_drawls('ba:na:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_empty_string(self):
        """Test remove_drawls with an empty string."""
        actual_output = CHATWordCleaner.remove_drawls('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_pauses_within_words-method.

    def test_remove_pauses_within_words_one_pause(self):
        """Test remove_pauses with 1 pause (^)."""
        actual_output = CHATWordCleaner.remove_pauses_within_words(
            'spa^ghetti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_multiple_pauses(self):
        """Test remove_pauses with 2 pauses (^)."""
        actual_output = CHATWordCleaner.remove_pauses_within_words(
            'spa^ghe^tti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_two_pauses_one_letter_in_between(self):
        """Test remove_pauses with two pauses separated by one letter."""
        actual_output = CHATWordCleaner.remove_pauses_within_words('m^a^t')
        desired_output = 'mat'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_pause_at_the_end(self):
        """Test remove_pauses with one pause at the end."""
        actual_output = CHATWordCleaner.remove_pauses_within_words('ma^')
        desired_output = 'ma'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = CHATWordCleaner.remove_pauses_within_words('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_blocking(self):
        """Test remove_pauses with blocking."""
        actual_output = CHATWordCleaner.remove_pauses_within_words('^hey')
        desired_output = '^hey'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_blocking-method. (≠ or ^)

    def test_remove_blocking_unequal_sign(self):
        """Test remove_blocking with an unequal sign as marker (≠)."""
        actual_output = CHATWordCleaner.remove_blocking(
            '≠hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_circumflex(self):
        """Test remove_blocking with a circumflex as marker (^)."""
        actual_output = CHATWordCleaner.remove_blocking(
            '^there')
        desired_output = 'there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_empty_string(self):
        """Test remove_blocking with an empty string."""
        actual_output = CHATWordCleaner.remove_blocking('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_fillers-method.

    def test_remove_filler_without_dash(self):
        """Test remove_filler without dash."""
        word = '&hu'
        actual_output = CHATWordCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_with_dash(self):
        """Test remove_fillers with dash."""
        word = '&-hu'
        actual_output = CHATWordCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_empty_string(self):
        """Test remove_fillers with 3 fillers (&-uh)."""
        word = ''
        actual_output = CHATWordCleaner.remove_filler(word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_ampersand_with_equal_sign(self):
        """Test remove_fillers with ampersand and equal sign."""
        word = '&=hu'
        actual_output = CHATWordCleaner.remove_filler(word)
        desired_output = '&=hu'
        self.assertEqual(actual_output, desired_output)
