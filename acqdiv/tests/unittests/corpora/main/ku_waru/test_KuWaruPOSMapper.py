import unittest

from acqdiv.parsers.corpora.main.ku_waru.KuWaruPOSMapper import KuWaruPOSMapper


class KuWaruPOSMapperTest(unittest.TestCase):

    def test_map_sfx_clitic_pos(self):
        pos = '=post'
        actual = KuWaruPOSMapper.map(pos)
        expected = 'sfx'
        self.assertEqual(actual, expected)

    def test_map_sfx_morpheme_pos(self):
        pos = '-v:FUT'
        actual = KuWaruPOSMapper.map(pos)
        expected = 'sfx'
        self.assertEqual(actual, expected)

    def test_map_pfx_pos(self):
        pos = 'dem'
        actual = KuWaruPOSMapper.map(pos)
        expected = 'PRODEM'
        self.assertEqual(actual, expected)

    def test_map_pos_ud(self):
        pos = 'dem'
        actual = KuWaruPOSMapper.map(pos, ud=True)
        expected = 'DET'
        self.assertEqual(actual, expected)

    def test_map_pos_ud_with_parentheses(self):
        pos = 'prt(BT)'
        actual = KuWaruPOSMapper.map(pos, ud=True)
        expected = 'PART'
        self.assertEqual(actual, expected)
