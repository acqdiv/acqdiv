import unittest

from acqdiv.parsers.corpora.main.japanese_miyata.cleaner \
    import JapaneseMiyataCleaner as Cl


class JapaneseMiyataCleanerTest(unittest.TestCase):

    def test_clean_gloss(self):
        gloss = 'PRES'
        actual = Cl.clean_gloss(gloss)
        expected = 'PRS'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'onoma'
        actual = Cl.clean_pos(pos)
        expected = 'IDEOPH'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'ptl.fina'
        actual = Cl.clean_pos_ud(pos_ud)
        expected = 'PART'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
