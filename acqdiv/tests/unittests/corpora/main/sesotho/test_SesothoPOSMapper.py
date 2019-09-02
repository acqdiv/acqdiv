import unittest

from acqdiv.parsers.corpora.main.sesotho.pos_mapper \
    import SesothoPOSMapper as Mp


class SesothoPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'loc'
        actual = Mp.map(pos)
        expected = 'ADV'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'ij'
        actual = Mp.map(pos)
        expected = 'INTJ'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = 'pfx'
        actual = Mp.map(pos)
        expected = 'pfx'

        self.assertEqual(actual, expected)

    def test_map4(self):
        pos = 'd'
        actual = Mp.map(pos, ud=True)
        expected = 'PRON'

        self.assertEqual(actual, expected)
