import unittest

from acqdiv.parsers.corpora.main.inuktitut.pos_mapper \
    import InuktitutPOSMapper as Mp


class InuktitutPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'IACT'
        actual = Mp.map(pos)
        expected = 'PTCL'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'VV|TNS'
        actual = Mp.map(pos)
        expected = 'sfx'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = 'WH'
        actual = Mp.map(pos, ud=True)
        expected = 'PRON'

        self.assertEqual(actual, expected)
