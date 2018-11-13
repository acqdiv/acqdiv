import unittest

from acqdiv.parsers.toolbox.readers.TuatschinReader import TuatschinReader \
    as Tr


class TestTuatschinReader(unittest.TestCase):

    # ---------- remove_punctuation_seg_tier ----------

    def test_remove_punctuation_seg_tier_comma_question_mark(self):
        seg_tier = 'NICE , RIGHT ?'
        actual_output = Tr.remove_punctuation_seg_tier(seg_tier)
        desired_output = 'NICE RIGHT'
        self.assertEqual(actual_output, desired_output)

    def test_remove_punctuation_seg_tier_other_punct(self):
        seg_tier = 'BE+IT'
        actual_output = Tr.remove_punctuation_seg_tier(seg_tier)
        desired_output = 'BE+IT'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_dot_repetitions_seg_tier ----------

    def test_remove_dot_repetitions_seg_tier(self):
        seg_tier = 'WHAT IS . . .'
        actual_output = Tr.remove_dot_repetitions_seg_tier(seg_tier)
        desired_output = 'WHAT IS'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknown_seg_tier ----------

    def test_unify_unknown_seg_tier(self):
        seg_tier = 'WHAT XXX THAT'
        actual_output = Tr.unify_unknown_seg_tier(seg_tier)
        desired_output = 'WHAT ??? THAT'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed_seg_tier ----------

    def test_null_untranscribed_seg_tier(self):
        seg_tier = 'XXX'
        actual_output = Tr.null_untranscribed_seg_tier(seg_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_seg_tier ----------

    def test_clean_seg_tier_untranscribed(self):
        seg_tier = 'XXX'
        actual_output = Tr.clean_seg_tier(seg_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier_unknown_question_mark(self):
        seg_tier = 'WHAT XXX THAT ?'
        actual_output = Tr.clean_seg_tier(seg_tier)
        desired_output = 'WHAT ??? THAT'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed_gloss_tier ----------

    def test_null_untranscribed_gloss_tier(self):
        gloss_tier = 'inv'
        seg_tier = 'XXX'
        actual_output = Tr.null_untranscribed_gloss_tier(gloss_tier, seg_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_unknown_gloss_tier ----------

    def test_unify_unknown_gloss_tier(self):
        gloss_tier = 'AAA inv AAA inv'
        seg_tier = 'WHAT XXX THAT XXX'
        actual_output = Tr.unify_unknown_gloss_tier(gloss_tier, seg_tier)
        desired_output = 'AAA ??? AAA ???'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_punct_inv ----------

    def test_remove_punct_inv(self):
        gloss_tier = 'AAA inv AAA inv'
        pos_tier = 'WHAT PUNCT THAT PUNCT'
        actual_output = Tr.remove_punct_inv(gloss_tier, pos_tier)
        desired_output = 'AAA AAA'
        self.assertEqual(actual_output, desired_output)
