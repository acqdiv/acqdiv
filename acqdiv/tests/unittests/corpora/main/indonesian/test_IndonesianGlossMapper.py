import unittest

from acqdiv.parsers.corpora.main.indonesian.gloss_mapper \
    import IndonesianGlossMapper as Mp


class IndonesianGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'new'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'EXCL'
        actual = Mp.map(gloss)
        expected = 'EXCLA'

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = 'N-'
        actual = Mp.map(gloss)
        expected = 'AV'

        self.assertEqual(actual, expected)

    def test_map4(self):
        gloss = '-IN'
        actual = Mp.map(gloss)
        expected = 'VOICE'

        self.assertEqual(actual, expected)
