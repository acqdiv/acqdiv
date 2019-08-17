import unittest

from acqdiv.parsers.corpora.main.russian.RussianPOSMapper \
    import RussianPOSMapper as Mp


class RussianPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'NAME'
        actual = Mp.map(pos)
        expected = 'N'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'V'
        actual = Mp.map(pos)
        expected = 'V'

        self.assertEqual(actual, expected)

    def test_map3(self):
        pos = 'PRO-PERS'
        actual = Mp.map(pos)
        expected = 'PRODEM'

        self.assertEqual(actual, expected)

    def test_map4(self):
        pos = 'PRO-PERS'
        actual = Mp.map(pos, ud=True)
        expected = 'PRON'

        self.assertEqual(actual, expected)
