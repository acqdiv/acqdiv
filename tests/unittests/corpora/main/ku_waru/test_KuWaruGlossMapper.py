import unittest

from acqdiv.parsers.corpora.main.ku_waru.gloss_mapper \
    import KuWaruGlossMapper


class KuWaruGlossMapperTest(unittest.TestCase):

    def test_map(self):
        gloss = 'ADD'
        actual = KuWaruGlossMapper.map(gloss)
        expected = 'COLL'

        self.assertEqual(actual, expected)

    def test_map_multi_word_gloss(self):
        gloss = 'that.ANA'
        actual = KuWaruGlossMapper.map(gloss)
        expected = 'DIST'

        self.assertEqual(actual, expected)

    def test_map_multi_lexical_gloss(self):
        gloss = 'come'
        actual = KuWaruGlossMapper.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map_multi_multiple_lexical_glosses(self):
        gloss = 'cute.thing'
        actual = KuWaruGlossMapper.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map_lexical_and_grammatical_glosses(self):
        gloss = 'do.IMP'
        actual = KuWaruGlossMapper.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map_bt_tp_lexical(self):
        gloss = 'brother.TP.BT'
        actual = KuWaruGlossMapper.map(gloss)
        expected = ''

        self.assertEqual(actual, expected)

    def test_map_bt_tp_grammatical(self):
        gloss = '2SG.BT'
        actual = KuWaruGlossMapper.map(gloss)
        expected = '2SG'

        self.assertEqual(actual, expected)

    def test_map_multiple_categories(self):
        gloss = '-FUT:2/3PL'
        actual = KuWaruGlossMapper.map(gloss)
        expected = 'FUT.2/3PL'

        self.assertEqual(actual, expected)

    def test_map_person_number_only(self):
        gloss = '1SG'
        actual = KuWaruGlossMapper.map(gloss)
        expected = '1SG'

        self.assertEqual(actual, expected)
