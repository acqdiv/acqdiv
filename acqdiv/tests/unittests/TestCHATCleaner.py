import unittest
from acqdiv.parsers.xml.CHATCleaner import CHATCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    Class to test the CHATCleaner.


    A lot of the test cases are taken from or inspired by
    https://talkbank.org/manuals/CHAT.pdf
    .
    """

    # Tests for the remove_redundant_whitespace-method.

    def test_leading_trailing_whitespace(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(' h '), 'h')

    def test_multiple_whitespace(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('  h  h  '), 'h h')

    def test_leading_trailing_tabs(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\th\t'), 'h')

    def test_multiple_tabs(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\t\th\t\th\t\t'), 'h h')

    def test_leading_trailing_newlines(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\nh\n'), 'h')

    def test_multiple_newlines(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\n\nh\n\nh\n\n'), 'h h')

    def test_leading_trailing_creturns(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\rh\r'), 'h')

    def test_multiple_creturns(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\r\rh\r\rh\r\r'), 'h h')

    def test_combinations(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\n\t \r\r h   \nh \t\t\n\r'), 'h h')

    # Tests for the remove_terminator-method.

    def test_period(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            'I got cold.'), 'I got cold')

    def test_question_mark(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*FAT: is that a carrot?'), '*FAT: is that a carrot')

    def test_exclamation_point(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT: sit down!'), '*MOT: sit down')

    def test_trailing_off(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +...'),
            '*SAR: smells good enough for')

    def test_trailing_off_of_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +..?'),
            '*SAR: smells good enough for')

    def test_question_with_exclamation(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?'),
            '*SAR: smells good enough for this')

    def test_interruption(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/.'), '*MOT:what did you')

    def test_interruption_of_a_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/?'), '*MOT:what did you')

    def test_self_interruption(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for +//.'),
            '*SAR:smells good enough for')

    def test_self_interrupted_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +//?'), '*MOT:what did you')

    def test_transcription_break(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for me +.'),
            '*SAR:smells good enough for me')

    def test_CA_terminator(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            'what did you ++.'), 'what did you')

    def test_CA_begin_latch(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            'what did you +=.'), 'what did you')

    def test_quotation_on_next_line(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*CHI:and then the little bear said +”/.'),
            '*CHI:and then the little bear said')

    def test_quotation_precedes(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '+” please give me all of your honey.'),
            'please give me all of your honey.')

    # Tests for the null_untranscribed_utterances-method.

    def test_xxx(self):
        self.assertEqual(CHATCleaner.null_untranscribed_utterances('xxx'), '')

    def test_normal_utt(self):
        self.assertEqual(CHATCleaner.null_untranscribed_utterances(
            'Hey there'), 'Hey there')

    # Tests for the null_event_utterances-method.

    def test_null(self):
        self.assertEqual(CHATCleaner.null_event_utterances('0'), '')

    def test_normal_utt_event(self):
        self.assertEqual(CHATCleaner.null_event_utterances(
            'Hey there'), 'Hey there')

    # Tests for the remove_events-method.

    def test_single_event(self):
        self.assertEqual(CHATCleaner.remove_events(
            'Hey there &=coughs'), 'Hey there')

    def test_multiple_events(self):
        self.assertEqual(CHATCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes.'), 'I got cold.')

    # Tests for the handle_repetitions-method.
    # should I test for bad notation like negative numbers?

    def test_single_repetition(self):
        self.assertEqual(CHATCleaner.handle_repetitions(
            "it's [x 4] like a um dog."), "it's it's it's it's like a um dog.")

    def test_multiple_repetitions(self):
        self.assertEqual(CHATCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]'), 'Hey Hey there there there')

    # Tests for the remove_omissions-method.

    def test_single_omission(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is my truck?'), 'where my truck?')

    def test_multiple_omissions(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is 0my truck?'), 'where truck?')

    def test_omission_with_marker(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is [*] my truck?'), 'where my truck?')

    # Tests for the unify_untranscribed-method.

    def test_untranscribed_xyz(self):
        self.assertEqual(CHATCleaner.unify_untranscribed(
            'zzz xxx yyy truck?'), 'xxx xxx xxx truck?')

    # Tests for the remove_form_markers-method.

    def test_l_marked(self):
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's m@l a@l r@l k@l."), "it's m a r k.")

    def test_k_marked(self):
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's mark@k."), "it's mark.")

    # Test for the remove_linkers-method.

    def test_quoted_utterance_linker_no_slash(self):
        self.assertEqual(CHATCleaner.remove_linkers('+". where is  my truck?'),
                         'where my truck?')

    def test_quoted_utterance_linker_with_slash(self):
        self.assertEqual(CHATCleaner.remove_linkers(
            '+"/. where is  my truck?'), 'where is  my truck?')

    def test_quick_uptake_linker(self):
        self.assertEqual(CHATCleaner.remove_linkers('+^ where is  my truck?'),
                         'where is  my truck?')

    def test_lazy_overlap_marking_linker(self):
        self.assertEqual(CHATCleaner.remove_linkers(
            '+< they had to go in here.'), 'they had to go in here.')

    def test_self_completion_linker(self):
        self.assertEqual(CHATCleaner.remove_linkers('+, I go straight ahead.'),
                         'I go straight ahead.')

    def test_other_completion_linker(self):
        self.assertEqual(CHATCleaner.remove_linkers('++ he would have come.'),
                         'he would have come.')

    # Tests for the remove_separators-method.

    def test_comma_colon_semi(self):
        self.assertEqual(CHATCleaner.remove_separators(
            'Hey there , what ; up : no'),
            'Hey there what up no')

    # Tests for the remove_ca-method.

    def test_falling_rising_mark(self):
        self.assertEqual(CHATCleaner.remove_separators(
            'Hey there ↓ what up ↑ no ↓↑'),
            'Hey there what up no')

    def test_marked_question(self):
        self.assertEqual(CHATCleaner.remove_separators(
            'Hey there„ what up no'),
            'Hey there what up no')

    def test_question_rise_intonation_mark(self):
        self.assertEqual(CHATCleaner.remove_separators(
            'Hey there ¿ what up no'),
            'Hey there what up no')

    # Tests for the remove_fillers-method.

    def test_remove_fillers(self):
        self.assertEqual(CHATCleaner.remove_fillers('&-uh &-uh the water'),
                         'uh uh the water')

    # Tests for the remove_pauses_within_words-method.

    def test_one_pause_within_word(self):
        self.assertEqual(CHATCleaner.remove_pauses_within_words('spa^ghetti'),
                         'spaghetti')

    def test_multiple_pauses_within_words(self):
        self.assertEqual(CHATCleaner.remove_pauses_within_words(
            'spa^ghe^tti bologne^se'),
            'spaghetti bolognese')

    # Test for the remove_blocking-method. (≠ or ^)

    def test_remove_blocking(self):
        self.assertEqual(CHATCleaner.remove_blocking(
            '≠hey ^there'),
            'hey there')

    # Test for the remove_pauses_between_words-method.

    def test_remove_pauses_betwee_words(self):
        self.assertEqual(CHATCleaner.remove_pauses_between_words(
            "I (.) don't (..) know (...) this."),
            "I don't know this.")

    # Tests for the remove_drawls-method.

    def test_lengthened_syllable(self):
        self.assertEqual(CHATCleaner.remove_drawls('bana:nas'), 'bananas')

    def test_pause_between_syllables(self):
        self.assertEqual(CHATCleaner.remove_drawls('rhi^noceros'),
                         'rhi^noceros')

    # Test for the remove_scoped_symbols-method.

    def test_remove_scoped_symbols(self):
        self.assertEqual(CHATCleaner.remove_scoped_symbols(
            "<that's mine> [=! cries]"),
            "that's mine")  # should the 'cries' remain in the string?


class TestInuktutCleaner(unittest.TestCase):
    """class to test the InuktutCleaner.
    """

    


if __name__ == '__main__':
    unittest.main()
