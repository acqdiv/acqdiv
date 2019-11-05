import unittest

from acqdiv.parsers.corpora.main.tuatschin.pos_mapper \
    import TuatschinPOSMapper as TM


class TuatschinPOSMapperTest(unittest.TestCase):

    def test_map1_pos(self):
        pos = 'DET_Art_Ind'
        actual_output = TM.map(pos)
        desired_output = 'ART'
        self.assertEqual(actual_output, desired_output)

    def test_map2_pos(self):
        pos = 'NOUN_Chld'
        actual_output = TM.map(pos)
        desired_output = 'N'
        self.assertEqual(actual_output, desired_output)

    def test_map3_pos(self):
        pos = 'VERB+DET_Art_Def'
        actual_output = TM.map(pos)
        desired_output = 'V+ART'
        self.assertEqual(actual_output, desired_output)

    def test_map4_pos_ud(self):
        pos = 'VERB+DET_Art_Def'
        actual_output = TM.map(pos, ud=True)
        desired_output = 'VERB+DET'
        self.assertEqual(actual_output, desired_output)

    def test_map5_pos_ud(self):
        pos = 'PROPN'
        actual_output = TM.map(pos, ud=True)
        desired_output = 'PROPN'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_pos ----------

    def test_clean_pos(self):
        pos = 'ADP_Chld'
        actual_output = TM.clean_pos(pos)
        desired_output = 'ADP'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_specifications ----------

    def test_remove_specifications_single(self):
        pos = 'ADP_Chld'
        actual_output = TM.remove_specifications(pos)
        desired_output = 'ADP'
        self.assertEqual(actual_output, desired_output)

    def test_remove_specifications_multiple(self):
        pos = 'ADP+DET_Art_Def'
        actual_output = TM.remove_specifications(pos)
        desired_output = 'ADP+DET'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
