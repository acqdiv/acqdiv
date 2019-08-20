import unittest

from acqdiv.parsers.corpora.main.inuktitut.InuktitutGlossMapper \
    import InuktitutGlossMapper as Mp


class InuktitutGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'here'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'CSV_3sS'
        actual = Mp.map(gloss)
        expected = 'CONTING.3SG.S'

        self.assertEqual(actual, expected)
