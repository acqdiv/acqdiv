import unittest

from acqdiv.parsers.corpora.main.yucatec.YucatecCleaner import YucatecCleaner


class TestYucatecCleaner(unittest.TestCase):

    # ---------- correct_hyphens ----------

    def test_correct_hyphens(self):
        """Test correct_hyphens."""
        morph_tier = 'STEM|stem:SFX-sfx'
        actual_output = YucatecCleaner.correct_hyphens(morph_tier)
        desired_output = 'STEM|stem:SFX|sfx'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_colon ----------

    def test_remove_colon_trailing(self):
        """Test remove_colon with trailing colon."""
        word = 'PFX:GLOSS|prefix#STEM:POS|stem:'
        actual_output = YucatecCleaner.remove_colon(word)
        desired_output = 'PFX:GLOSS|prefix#STEM:POS|stem'
        self.assertEqual(actual_output, desired_output)

    def test_remove_colon_leading(self):
        """Test remove_colon with leading colon."""
        word = ':STEM|stem'
        actual_output = YucatecCleaner.remove_colon(word)
        desired_output = 'STEM|stem'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_dash ----------

    def test_remove_dash_trailing(self):
        """Test remove_dash with leading colon."""
        word = 'STEM|stem-'
        actual_output = YucatecCleaner.remove_dash(word)
        desired_output = 'STEM|stem'
        self.assertEqual(actual_output, desired_output)

    def test_remove_dash_leading(self):
        """Test remove_dash with leading colon."""
        word = 'STEM|stem-'
        actual_output = YucatecCleaner.remove_dash(word)
        desired_output = 'STEM|stem'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_colon_dash ----------

    def test_remove_colon_dash(self):
        """Test remove_colon_dash with leading colon."""
        word = 'STEM|stem:-'
        actual_output = YucatecCleaner.remove_colon_dash(word)
        desired_output = 'STEM|stem'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = '2POSS:SG'
        actual = YucatecCleaner.clean_gloss(gloss)
        expected = '2SG.POSS'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'V:TRANS'
        actual = YucatecCleaner.clean_pos(pos)
        expected = 'V'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'V:TRANS'
        actual = YucatecCleaner.clean_pos_ud(pos_ud)
        expected = 'VERB'
        self.assertEqual(actual, expected)