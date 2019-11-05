import unittest

from acqdiv.parsers.corpora.main.russian.gloss_mapper \
    import RussianGlossMapper as Mp


class RussianGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = 'M:SG:NOM:AN'
        actual = Mp.map(gloss)
        expected = 'M.SG.NOM.ANIM'

        self.assertEqual(actual, expected)

    def test_map2(self):
        gloss = 'xxx'
        actual = Mp.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map3(self):
        gloss = 'IMP:2:SG:IRREFL:IPFV'
        actual = Mp.map(gloss)
        expected = 'IPFV.IMP.2SG'

        self.assertEqual(actual, expected)
