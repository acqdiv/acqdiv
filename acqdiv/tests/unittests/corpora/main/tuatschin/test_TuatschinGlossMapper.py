import unittest

from acqdiv.parsers.corpora.main.tuatschin.TuatschinGlossMapper \
    import TuatschinGlossMapper as TM


class TuatschinGlossMapperTest(unittest.TestCase):

    def map1(self):
        gloss = 'VERB.2.Sing.Ind.Pres'
        actual_output = TM.map(gloss)
        desired_output = '2SG.IND.PRS'
        self.assertEqual(actual_output, desired_output)

    def map2(self):
        gloss = 'inv'
        actual_output = TM.map(gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def map3(self):
        gloss = 'DET.Masc.Sing'
        actual_output = TM.map(gloss)
        desired_output = 'M.SG'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_gloss ----------

    def test_clean_gloss(self):
        gloss = 'ADJ.Fem.Sing'
        actual_output = TM.clean_gloss(gloss)
        desired_output = 'Fem.Sing'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_pos ----------

    def test_remove_pos(self):
        gloss = 'ADJ.Fem.Sing'
        actual_output = TM.remove_pos(gloss)
        desired_output = 'Fem.Sing'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
