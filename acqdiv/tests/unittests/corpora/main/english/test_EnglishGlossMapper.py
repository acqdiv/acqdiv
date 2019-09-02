import unittest

from acqdiv.parsers.corpora.main.english.gloss_mapper \
    import EnglishGlossMapper as Mp


class EnglishGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'put&ZERO'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'PRESP'
        actual = Mp.map(gloss)
        expected = 'PRS'

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = 'test'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)
