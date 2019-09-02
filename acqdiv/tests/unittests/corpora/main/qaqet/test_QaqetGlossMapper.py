import unittest

from acqdiv.parsers.corpora.main.qaqet.gloss_mapper \
    import QaqetGlossMapper as QM


class QaqetGlossMapperTest(unittest.TestCase):

    def test_map1(self):
        gloss = '2SG.SBJ.NPST='
        actual_output = QM.map(gloss)
        desired_output = '2SG.SBJ.NPST'
        self.assertEqual(actual_output, desired_output)

    def test_map2(self):
        gloss = 'do/act:IN'
        actual_output = QM.map(gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
