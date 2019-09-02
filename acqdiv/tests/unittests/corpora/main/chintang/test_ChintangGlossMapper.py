import unittest

from acqdiv.parsers.corpora.main.chintang.gloss_mapper \
    import ChintangGlossMapper as CM


class ChintangGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'cry'
        actual = CM.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = '-1/2pS/P'
        actual = CM.map(gloss)
        expected = '1/2PL.S/P'

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = '***'
        actual = CM.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map4(self):
        gloss = '-DEM.ACROSS'
        actual = CM.map(gloss)
        expected = 'DEM.ACROSS'

        self.assertEqual(actual, expected)
