import unittest

from acqdiv.parsers.corpora.main.sesotho.SesothoGlossMapper \
    import SesothoGlossMapper as Mp


class SesothoGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'sm2s'
        actual = Mp.map(gloss)
        expected = '2SG.SBJ'

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'm^i'
        actual = Mp.map(gloss)
        expected = 'IMP'

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = 'if'
        actual = Mp.map(gloss)
        expected = 'COND'

        self.assertEqual(actual, expected)

    def test_map4(self):
        gloss = 'thing(9,10)'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_remove_nominal_concord_markers_empty_string(self):
        """Test remove_nominal_concord_markers with an empty string."""
        gloss = ''
        actual_output = Mp.remove_nominal_concord_markers(
            gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_word(self):
        """Test unify_untranscibed_glosses with 'word'."""
        gloss = 'word'
        actual_output = Mp.unify_untranscribed_glosses(gloss)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_xxx(self):
        """Test unify_untranscibed_glosses with 'xxx'."""
        gloss = 'xxx'
        actual_output = Mp.unify_untranscribed_glosses(gloss)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_empty_string(self):
        """Test unify_untranscibed_glosses with empty string."""
        gloss = ''
        actual_output = Mp.unify_untranscribed_glosses(gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_nominal_concord_markers_single(self):
        """Test remove_nominal_concord_markers with 1 concord marker."""
        gloss = 'obr17'
        actual_output = Mp.remove_nominal_concord_markers(
            gloss)
        desired_output = '17'
        self.assertEqual(actual_output, desired_output)

    def test_remove_noun_markers_with_marker(self):
        """Test remove_noun_markers with noun_marker."""
        gloss_word = 'n^6-field(9 , 6)'
        actual_output = Mp.remove_noun_markers(gloss_word)
        desired_output = '6-field(9 , 6)'
        self.assertEqual(actual_output, desired_output)

    def test_remove_noun_markers_empty_string(self):
        """Test remove_noun_markers with empty string."""
        gloss_word = ''
        actual_output = Mp.remove_noun_markers(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_verb_markers_with_marker(self):
        """Test remove_verb_markers with verb_marker."""
        gloss_word = 'sm2s-t^p_v^do-m^in'
        actual_output = Mp.remove_verb_markers(gloss_word)
        desired_output = 'sm2s-t^p_do-m^in'
        self.assertEqual(actual_output, desired_output)

    def test_remove_verb_markers_empty_string(self):
        """Test remove_verb_markers with empty string."""
        gloss_word = ''
        actual_output = Mp.remove_verb_markers(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_name(self):
        """Test clean_proper_names_gloss_words with a name."""
        gloss_word = 'n^Name'
        actual_output = Mp.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'a_name'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_game(self):
        """Test clean_proper_names_gloss_words with a game."""
        gloss_word = 'n^Place'
        actual_output = Mp.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'a_place'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_no_proper_name(self):
        """Test clean_proper_names_gloss_words with not a proper name."""
        gloss_word = 'sm1s-t^p_v^be_sick-m^x'
        actual_output = Mp.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'sm1s-t^p_v^be_sick-m^x'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_empty_string(self):
        """Test clean_proper_names_gloss_words with an empty string."""
        gloss_word = ''
        actual_output = Mp.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)
