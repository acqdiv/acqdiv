import unittest

from acqdiv.parsers.corpora.main.chintang.ChintangPOSMapper \
    import ChintangPOSMapper as CM


class ChintangPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = '-gm'
        actual = CM.map(pos)
        expected = 'sfx'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'vi'
        actual = CM.map(pos)
        expected = 'V'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = 'gm'
        actual = CM.map(pos)
        expected = 'PTCL'

        self.assertEqual(actual, expected)

    def test_map4(self):
        pos = 'gm'
        actual = CM.map(pos, ud=True)
        expected = 'PART'

        self.assertEqual(actual, expected)
