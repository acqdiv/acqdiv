import unittest

from acqdiv.parsers.corpora.main.cree.pos_mapper \
    import CreePOSMapper as Mp


class CreePOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'dem.pxl'
        actual = Mp.map(pos)
        expected = 'PRODEM'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'dem+G.dst'
        actual = Mp.map(pos)
        expected = 'PRODEM'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = 'dem.pxl'
        actual = Mp.map(pos, ud=True)
        expected = 'PRON'

        self.assertEqual(actual, expected)

    def test_uppercase_pos_in_parentheses_one_parenth_pair(self):
        """Test uppercase_pos_in_parentheses with one pair."""
        pos = 'na eˈp~o~(h)'
        actual_output = Mp.uppercase_pos_in_parentheses(pos)
        desired_output = 'na eˈp~o~(H)'
        self.assertEqual(actual_output, desired_output)

    def test_uppercase_pos_in_parentheses_empty_string(self):
        """Test uppercase_pos_in_parentheses with empty string."""
        actual_output = Mp.uppercase_pos_in_parentheses('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)
