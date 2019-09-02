import unittest

from acqdiv.parsers.corpora.main.nungon.gloss_mapper \
    import NungonGlossMapper as Mp


class NungonGlossMapperTest(unittest.TestCase):

    # ---------- replace_slash ----------

    def test_replace_slash_slash_between_numbers(self):
        """Test replace_slash with slash between numbers."""
        gloss = '2/3pl'
        actual_output = Mp.replace_slash(gloss)
        desired_output = '2.3pl'
        self.assertEqual(actual_output, desired_output)

    def test_replace_slash_slash_not_between_numbers(self):
        """Test replace_slash with slash not between numbers."""
        gloss = 'test/test'
        actual_output = Mp.replace_slash(gloss)
        desired_output = 'test/test'
        self.assertEqual(actual_output, desired_output)

    def test_replace_plus(self):
        """Test replace_plus."""
        gloss = '1sg+ben'
        actual_output = Mp.replace_plus(gloss)
        desired_output = '1sg.ben'
        self.assertEqual(actual_output, desired_output)
