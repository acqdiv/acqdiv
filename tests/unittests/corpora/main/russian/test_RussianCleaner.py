import unittest

from acqdiv.parsers.corpora.main.russian.cleaner \
    import RussianCleaner as Cl


class RussianCleanerTest(unittest.TestCase):

    def test_clean_gloss(self):
        gloss = 'M:SG:NOM:AN'
        actual = Cl.clean_gloss(gloss)
        expected = 'M.SG.NOM.ANIM'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'PRO-PERS'
        actual = Cl.clean_pos(pos)
        expected = 'PRODEM'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'PRO-PERS'
        actual = Cl.clean_pos_ud(pos_ud)
        expected = 'PRON'
        self.assertEqual(actual, expected)
