import unittest

from acqdiv.parsers.corpora.main.english.EnglishManchester1Cleaner \
    import EnglishManchester1Cleaner as Cl


class ChintangCleanerTest(unittest.TestCase):

    def test_clean_gloss(self):
        gloss = 'PRESP'
        actual = Cl.clean_gloss(gloss)
        expected = 'PRS'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'pro:int'
        actual = Cl.clean_pos(pos)
        expected = 'PRODEM'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'pro:int'
        actual = Cl.clean_pos_ud(pos_ud)
        expected = 'PRON'
        self.assertEqual(actual, expected)
