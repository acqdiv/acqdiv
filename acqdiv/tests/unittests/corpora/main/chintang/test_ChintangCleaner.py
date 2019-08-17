import unittest

from acqdiv.parsers.corpora.main.chintang.ChintangCleaner \
    import ChintangCleaner as Cl


class ChintangCleanerTest(unittest.TestCase):

    def test_clean_gloss(self):
        gloss = '-1/2pS/P'
        actual = Cl.clean_gloss(gloss)
        expected = '1/2PL.S/P'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'vi'
        actual = Cl.clean_pos(pos)
        expected = 'V'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'vi'
        actual = Cl.clean_pos_ud(pos_ud)
        expected = 'VERB'
        self.assertEqual(actual, expected)
