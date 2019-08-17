import unittest

from acqdiv.parsers.corpora.main.qaqet.QaqetPOSMapper \
    import QaqetPOSMapper as QM


class QaqetPOSMapperTest(unittest.TestCase):

    def test_map1(self):
        pos = '-PRO'
        actual_output = QM.map(pos)
        desired_output = 'sfx'
        self.assertEqual(actual_output, desired_output)

    def test_map2(self):
        pos = 'V.CONT'
        actual_output = QM.map(pos)
        desired_output = 'V'
        self.assertEqual(actual_output, desired_output)

    def test_map3(self):
        pos = 'V.NCONT.FUT'
        actual_output = QM.map(pos, ud=True)
        desired_output = 'VERB'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknowns_morpheme ----------

    def test_unify_unknowns_morpheme_question_mark(self):
        morpheme = '??'
        actual_output = QM.unify_unknowns_morpheme(morpheme)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknowns_morpheme_xxx(self):
        morpheme = 'xxx'
        actual_output = QM.unify_unknowns_morpheme(morpheme)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknowns_morpheme_x(self):
        morpheme = 'x'
        actual_output = QM.unify_unknowns_morpheme(morpheme)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknowns_morpheme_sfx(self):
        morpheme = 'sfx'
        actual_output = QM.unify_unknowns_morpheme(morpheme)
        desired_output = 'sfx'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknowns_morpheme_pfx(self):
        morpheme = 'pfx'
        actual_output = QM.unify_unknowns_morpheme(morpheme)
        desired_output = 'pfx'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
