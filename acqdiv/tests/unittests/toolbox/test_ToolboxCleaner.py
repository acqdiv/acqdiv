import unittest
from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner


class TestToolboxCleaner(unittest.TestCase):

    def test_remove_redundant_whitespaces(self):
        string = '  no such     thing       '
        actual_output = ToolboxCleaner.remove_redundant_whitespaces(string)
        desired_output = 'no such thing'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_xxx(self):
        utterance = 'xxx are xxx'
        actual_output = ToolboxCleaner.unify_unknown(utterance)
        desired_output = '??? are ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_www(self):
        utterance = 'here www examples'
        actual_output = ToolboxCleaner.unify_unknown(utterance)
        desired_output = 'here ??? examples'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_stars(self):
        utterance = 'here *** examples'
        actual_output = ToolboxCleaner.unify_unknown(utterance)
        desired_output = 'here ??? examples'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_xxx_stars_www(self):
        utterance = 'xxx *** www, ***'
        actual_output = ToolboxCleaner.unify_unknown(utterance)
        desired_output = '??? ??? ???, ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_empty_string(self):
        utterance = ''
        actual_output = ToolboxCleaner.unify_unknown(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_stars_xxx(self):
        utterance = 'These *** some good xxx .'
        actual_output = ToolboxCleaner.clean_utterance(utterance)
        desired_output = 'These ??? some good ??? .'
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        utterance = ''
        actual_output = ToolboxCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- utterance word ----------

    def test_clean_word_xxx(self):
        utterance = 'xxx-less'
        actual_output = ToolboxCleaner.clean_utterance(utterance)
        desired_output = '???-less'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_empty_string(self):
        utterance = ''
        actual_output = ToolboxCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- morphology tiers ----------

    def test_clean_morph_tier(self):
        morph_tier = 'the morph tier'
        actual_output = ToolboxCleaner.clean_morph_tier(morph_tier)
        desired_output = 'the morph tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        seg_tier = 'the seg tier'
        actual_output = ToolboxCleaner.clean_seg_tier(seg_tier)
        desired_output = 'the seg tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        gloss_tier = 'the gloss tier'
        actual_output = ToolboxCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'the gloss tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        pos_tier = 'the pos tier'
        actual_output = ToolboxCleaner.clean_pos_tier(pos_tier)
        desired_output = 'the pos tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang_tier(self):
        lang_tier = 'the lang tier'
        actual_output = ToolboxCleaner.clean_lang_tier(lang_tier)
        desired_output = 'the lang tier'
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme words ----------

    def test_clean_morpheme_word(self):
        morpheme_word = 'mor-word'
        actual_output = ToolboxCleaner.clean_morpheme_word(morpheme_word)
        desired_output = 'mor-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word(self):
        seg_word = 'seg-word'
        actual_output = ToolboxCleaner.clean_seg_word(seg_word)
        desired_output = 'seg-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_word(self):
        gloss_word = 'gloss-word'
        actual_output = ToolboxCleaner.clean_gloss_word(gloss_word)
        desired_output = 'gloss-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_word(self):
        pos_word = 'pos-word'
        actual_output = ToolboxCleaner.clean_pos_word(pos_word)
        desired_output = 'pos-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang_word(self):
        lang_word = 'lang-word'
        actual_output = ToolboxCleaner.clean_lang_word(lang_word)
        desired_output = 'lang-word'
        self.assertEqual(actual_output, desired_output)

    # ---------- morphemes ----------

    def test_clean_morpheme(self):
        morpheme = 'morpheme'
        actual_output = ToolboxCleaner.clean_morpheme(morpheme)
        desired_output = 'morpheme'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg(self):
        seg = 'seg'
        actual_output = ToolboxCleaner.clean_seg(seg)
        desired_output = 'seg'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = 'gloss'
        actual_output = ToolboxCleaner.clean_gloss_raw(gloss)
        desired_output = 'gloss'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos(self):
        pos = 'pos'
        actual_output = ToolboxCleaner.clean_pos_raw(pos)
        desired_output = 'pos'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang(self):
        lang = 'lang'
        actual_output = ToolboxCleaner.clean_lang(lang)
        desired_output = 'lang'
        self.assertEqual(actual_output, desired_output)
