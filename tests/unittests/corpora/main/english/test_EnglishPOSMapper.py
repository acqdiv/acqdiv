import unittest

from acqdiv.parsers.corpora.main.english.pos_mapper \
    import EnglishPOSMapper as Mp


class EnglishPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = 'pro:int'
        actual = Mp.map(pos)
        expected = 'PRODEM'

        self.assertEqual(actual, expected)

    def test_map2(self):
        pos = 'aux'
        actual = Mp.map(pos)
        expected = 'AUX'

        self.assertEqual(actual, expected)

    def test_map4(self):
        pos = 'pro:int'
        actual = Mp.map(pos, ud=True)
        expected = 'PRON'

        self.assertEqual(actual, expected)
