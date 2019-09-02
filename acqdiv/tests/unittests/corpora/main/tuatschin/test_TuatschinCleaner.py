import unittest

from acqdiv.parsers.corpora.main.tuatschin.cleaner \
    import TuatschinCleaner as Tc


class TestTuatschinCleaner(unittest.TestCase):

    # ---------- remove_punctuation_seg_tier ----------

    def test_remove_punctuation_seg_tier_comma_question_mark(self):
        seg_tier = 'NICE , RIGHT ?'
        actual_output = Tc.remove_punctuation_seg_tier(seg_tier)
        desired_output = 'NICE RIGHT'
        self.assertEqual(actual_output, desired_output)

    def test_remove_punctuation_seg_tier_other_punct(self):
        seg_tier = 'BE+IT'
        actual_output = Tc.remove_punctuation_seg_tier(seg_tier)
        desired_output = 'BE+IT'
        self.assertEqual(actual_output, desired_output)

    def test_remove_punctuation_seg_tier_dot(self):
        seg_tier = 'test . test'
        actual_output = Tc.remove_punctuation_seg_tier(seg_tier)
        desired_output = 'test test'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_dot_repetitions_seg_tier ----------

    def test_remove_dot_repetitions_seg_tier(self):
        seg_tier = 'WHAT IS . . .'
        actual_output = Tc.remove_dot_repetitions_seg_tier(seg_tier)
        desired_output = 'WHAT IS'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknown_seg_tier ----------

    def test_unify_unknown_seg_tier(self):
        seg_tier = 'WHAT XXX THAT'
        actual_output = Tc.unify_unknown_seg_tier(seg_tier)
        desired_output = 'WHAT ??? THAT'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_seg_tier ----------

    def test_clean_seg_tier_unknown(self):
        seg_tier = 'XXX'
        actual_output = Tc.clean_seg_tier(seg_tier)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier_unknown_question_mark(self):
        seg_tier = 'WHAT XXX THAT ?'
        actual_output = Tc.clean_seg_tier(seg_tier)
        desired_output = 'WHAT ??? THAT'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknown_gloss_tier ----------

    def test_unify_unknown_gloss_tier(self):
        gloss_tier = 'AAA inv AAA inv'
        seg_tier = 'WHAT XXX THAT XXX'
        actual_output = Tc.unify_unknown_gloss_tier(gloss_tier, seg_tier)
        desired_output = 'AAA ??? AAA ???'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_punct_inv ----------

    def test_remove_punct_inv(self):
        gloss_tier = 'AAA inv AAA inv'
        pos_tier = 'WHAT PUNCT THAT PUNCT'
        actual_output = Tc.remove_punct_inv(gloss_tier, pos_tier)
        desired_output = 'AAA AAA'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_punct_inv ----------

    def test_unify_unknown_pos_tier_none(self):
        pos_tier = 'N AUX V'
        actual_output = Tc.unify_unknown_pos_tier(pos_tier)
        desired_output = 'N AUX V'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_pos_tier(self):
        pos_tier = 'N X V'
        actual_output = Tc.unify_unknown_pos_tier(pos_tier)
        desired_output = 'N ??? V'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_pos_tier_Chld(self):
        pos_tier = 'N X_Chld V'
        actual_output = Tc.unify_unknown_pos_tier(pos_tier)
        desired_output = 'N ??? V'
        self.assertEqual(actual_output, desired_output)

    # ---------- lowercase_seg_word ----------

    def test_lowercase_seg_word(self):
        seg_word = 'PLÉDACÙVAGNÌ+IÈ'
        actual_output = Tc.lowercase_seg_word(seg_word)
        desired_output = 'plédacùvagnì+iè'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_seg_word ----------

    def test_clean_seg_word(self):
        seg_word = 'PLÉDACÙVAGNÌ+IÈ'
        actual_output = Tc.clean_seg_word(seg_word)
        desired_output = 'plédacùvagnì+iè'
        self.assertEqual(actual_output, desired_output)
