import unittest

from acqdiv.parsers.inuktitut.InuktitutCleaner import InuktitutCleaner


class TestInuktitutCleaner(unittest.TestCase):
    """class to test the InuktitutCleaner."""

    def test_add_birth_date(self):
        metadata = ('ALI', 'Alec', '1984-01-01')
        actual_output = InuktitutCleaner.add_birth_date(*metadata)
        desired_output = '1986-08-25'
        self.assertEqual(actual_output, desired_output)

    # ---------- word cleaning ----------

    # Tests for the remove_dashes-method.

    def test_remove_dashes_standard_case(self):
        """Test remove_dashes for a standard case (Taku-xxx-nga)."""
        actual_output = InuktitutCleaner.remove_dashes('Taku-xxx-nga')
        desired_output = 'Takuxxxnga'
        self.assertEqual(actual_output, desired_output)

    def test_remove_dashes_empty_string(self):
        """Test remove_dashes for an empty string."""
        actual_output = InuktitutCleaner.remove_dashes('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the clean_word-method.

    def test_clean_word_standard(self):
        """Test clean_word for an already clean word."""
        str_input = 'majuratualui'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_utt_with_with_form_markers(self):
        """Test clean_word for an already clean word."""
        str_input = 'majuratualui@k'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_utt_with_drawls(self):
        """Test clean_word with drawls (two lengthend syllables)."""
        str_input = 'maju:ratua:lui'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_utt_with_blocking(self):
        """Test clean_word with blocking before word (^)."""
        str_input = '^majuratualui'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_pauses_within_words(self):
        """Test clean_word with 2 pauses within words (^)."""
        str_input = 'maj^uratua^lui'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_utt_mixed_markers(self):
        """Test clean_word with 2 pauses within words (^)."""
        str_input = '^maj^uratua:lui@l'
        actual_output = InuktitutCleaner.clean_word(str_input)
        desired_output = 'majuratualui'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_empty_string(self):
        """Test clean_word with an empty string."""
        actual_output = InuktitutCleaner.clean_word('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- morphology tier cleaning ----------

    @unittest.skip
    def test_clean_xmor_untranscribed_and_scoped_symbols_and_terminator(self):
        """Test clean_xmor with 3 cases at once.

        Cases: untranscribed material, terminator and scoped symbols
        """
        str_input = 'xxx ! [+ UI]'
        actual_output = InuktitutCleaner.clean_morph_tier(str_input)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_xmor_scoped_symbol_and_terminator(self):
        """Test clean_xmor with scoped symbols and terminator."""
        str_input = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+IACT|'
                     'ai^greetings . [+ IM]')
        actual_output = InuktitutCleaner.clean_morph_tier(str_input)
        desired_output = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+'
                          'IACT|ai^greetings')
        self.assertEqual(actual_output, desired_output)

    def test_clean_xmor_empty_string(self):
        """Test clean_xmor with an empty string."""
        str_input = ''
        actual_output = InuktitutCleaner.clean_morph_tier(str_input)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        """Test clean_seg_tier."""
        seg_tier = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+IACT|'
                    'ai^greetings . [+ IM]')
        actual_output = InuktitutCleaner.clean_seg_tier(seg_tier)
        desired_output = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+'
                          'IACT|ai^greetings')
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier."""
        seg_tier = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+IACT|'
                    'ai^greetings . [+ IM]')
        actual_output = InuktitutCleaner.clean_gloss_tier(seg_tier)
        desired_output = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+'
                          'IACT|ai^greetings')
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier."""
        seg_tier = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+IACT|'
                    'ai^greetings . [+ IM]')
        actual_output = InuktitutCleaner.clean_pos_tier(seg_tier)
        desired_output = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+'
                          'IACT|ai^greetings')
        self.assertEqual(actual_output, desired_output)

    # ---------- test morpheme cleaning ----------

    # Tests for the remove_english_marker-method.

    def test_remove_english_marker_single_marker(self):
        """Test remove_english_marker with 1 english marker (@e)."""
        str_input = 'NR|bag@e^bag NR|killak^hole+NN|lik^item_having .'
        actual_output = InuktitutCleaner.remove_english_marker(str_input)
        desired_output = 'NR|bag^bag NR|killak^hole+NN|lik^item_having .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_english_marker_multiple_markers(self):
        """Test remove_english_marker with 2 english markers (@e)."""
        str_input = 'PRO|you@e^you [/] PRO|you@e^you . [+SR]'
        actual_output = InuktitutCleaner.remove_english_marker(str_input)
        desired_output = 'PRO|you^you [/] PRO|you^you . [+SR]'
        self.assertEqual(actual_output, desired_output)

    def test_remove_english_marker_empty_string(self):
        """Test remove_english_marker with an empty string."""
        str_input = ''
        actual_output = InuktitutCleaner.remove_english_marker(str_input)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_segment(self):
        """Test clean_segment with an english marker."""
        actual_output = InuktitutCleaner.clean_segment('ka@e')
        desired_output = 'ka'
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_stem_gram_gloss_connector-method.

    def test_replace_stem_gram_gloss_connector_single_connector(self):
        """Test replace_stem_gram_gloss_connector with 1 connector."""
        input_str = 'FIL|am^um DR|u^here&SG_ST+DI|minga^MOD_SG [*] ?'
        actual_output = InuktitutCleaner.replace_stem_gram_gloss_connector(
            input_str)
        desired_output = 'FIL|am^um DR|u^here.SG_ST+DI|minga^MOD_SG [*] ?'
        self.assertEqual(actual_output, desired_output)

    def test_replace_stem_gram_gloss_connector_multiple_connectors(self):
        """Test replace_stem_gram_gloss_connector with 2 connectors."""
        gloss = 'NR|amaama^baby_bottle&BW NR|amaama^baby_bottle&BW'
        actual_output = InuktitutCleaner.replace_stem_gram_gloss_connector(
            gloss)
        desired_output = 'NR|amaama^baby_bottle.BW NR|amaama^baby_bottle.BW'
        self.assertEqual(actual_output, desired_output)

    def test_replace_stem_gram_gloss_connector_empty_string(self):
        """Test replace_stem_gram_gloss_connector with emtpy string."""
        actual_output = InuktitutCleaner.replace_stem_gram_gloss_connector('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        """Test clean_gloss with an english marker."""
        gloss = 'NR|amaama^baby_bottle&BW NR|amaama^baby_bottle&BW'
        actual_output = InuktitutCleaner.clean_gloss(gloss)
        desired_output = 'NR|amaama^baby_bottle.BW NR|amaama^baby_bottle.BW'
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_pos_separator-method.

    def test_replace_pos_separator_single_separator(self):
        """Test replace_pos_separator with 1 separator (|)."""
        pos = 'EXCL|ai^ACT ?'
        actual_output = InuktitutCleaner.replace_pos_separator(pos)
        desired_output = 'EXCL.ai^ACT ?'
        self.assertEqual(actual_output, desired_output)

    def test_replace_pos_separator_multiple_separators(self):
        """Test replace_pos_separator with 3 separators (|)."""
        pos = 'FIL|am^um DR|u^here&SG_ST+DI|minga^MOD_SG [*] ?'
        actual_output = InuktitutCleaner.replace_pos_separator(pos)
        desired_output = 'FIL.am^um DR.u^here&SG_ST+DI.minga^MOD_SG [*] ?'
        self.assertEqual(actual_output, desired_output)

    def test_replace_pos_separator_empty_string(self):
        """Test replace_pos_separator with an empty string."""
        actual_output = InuktitutCleaner.replace_pos_separator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos(self):
        """Test clean_pos with a separator (|)."""
        pos = 'EXCL|ai^ACT ?'
        actual_output = InuktitutCleaner.replace_pos_separator(pos)
        desired_output = 'EXCL.ai^ACT ?'
        self.assertEqual(actual_output, desired_output)