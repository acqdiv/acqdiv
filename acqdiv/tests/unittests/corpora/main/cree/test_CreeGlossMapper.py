import unittest

from acqdiv.parsers.corpora.main.cree.gloss_mapper \
    import CreeGlossMapper as Mp


class CreeGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'it.is.here'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'p,polar'
        actual = Mp.map(gloss)
        expected = 'Q'

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = '1s'
        actual = Mp.map(gloss)
        expected = '1SG'

        self.assertEqual(actual, expected)

    def test_replace_gloss_connector_multiple_plus_and_comma(self):
        """Test replace_gloss_connector with 2 commas and 2 pluses."""
        gloss = 'a,quest sm+gur2 a,quest sm+gur2'
        actual_output = Mp.replace_gloss_connector(gloss)
        desired_output = 'a.quest sm.gur2 a.quest sm.gur2'
        self.assertEqual(actual_output, desired_output)

    def test_replace_gloss_connector_empty_string(self):
        """Test replace_gloss_connector with empty string."""
        actual_output = Mp.replace_gloss_connector('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)
