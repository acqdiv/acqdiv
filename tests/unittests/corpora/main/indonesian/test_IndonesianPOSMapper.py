import unittest

from acqdiv.parsers.corpora.main.indonesian.pos_mapper \
    import IndonesianPOSMapper as Mp


class IndonesianPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'bye'
        actual = Mp.map(pos)
        expected = 'stem'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'N-'
        actual = Mp.map(pos)
        expected = 'pfx'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = '-IN'
        actual = Mp.map(pos)
        expected = 'sfx'

        self.assertEqual(actual, expected)

    def test_map4(self):
        pos = '-IN'
        actual = Mp.map(pos, ud=True)
        expected = ''

        self.assertEqual(actual, expected)
