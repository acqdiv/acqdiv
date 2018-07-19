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

    def test_remove_redundant_whitespace_leading_trailing_whitespace(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces(' h ')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_whitespace(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces('  h  h  ')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_tabs(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces('\th\t')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_tabs(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\t\th\t\th\t\t')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_newlines(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces('\nh\n')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_newlines(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\n\nh\n\nh\n\n')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_creturns(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces('\rh\r')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)


    def test_remove_redundant_whitespace_multiple_creturns(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\r\rh\r\rh\r\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_combinations(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\n\t \r\r h   \nh \t\t\n\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_empty_string(self):
        actual_output = CHATCleaner.remove_redundant_whitespaces('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_terminator-method.

    def test_remove_terminator_period(self):
        actual_output = CHATCleaner.remove_terminator('I got cold.')
        desired_output = 'I got cold'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_mark(self):
        actual_output = CHATCleaner.remove_terminator(
            '*FAT: is that a carrot?')
        desired_output = '*FAT: is that a carrot'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_exclamation_point(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT: sit down!'), '*MOT: sit down')

    def test_remove_terminator_trailing_off(self):
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +...')
        desired_output = '*SAR: smells good enough for'

    def test_remove_terminator_trailing_off_of_question(self):
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +..?')
        desired_output = '*SAR: smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_with_exclamation(self):
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?')
        desired_output = '*SAR: smells good enough for this'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption(self):
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +/.')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption_of_a_question(self):
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +/?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interruption(self):
        actual_output = CHATCleaner.remove_terminator(
            '*SAR:smells good enough for +//.')
        desired_output = '*SAR:smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interrupted_question(self):
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +//?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_transcription_break(self):
        actual_output = CHATCleaner.remove_terminator(
            '*SAR:smells good enough for me +.')
        desired_output = '*SAR:smells good enough for me'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_CA_terminator(self):
        actual_output = CHATCleaner.remove_terminator(
            'what did you ++.')
        desired_output = 'what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_CA_begin_latch(self):
        actual_output = CHATCleaner.remove_terminator(
            'what did you +=.')
        desired_output = 'what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_quotation_on_next_line(self):
        actual_output = CHATCleaner.remove_terminator(
            '*CHI:and then the little bear said +”/.')
        desired_output = '*CHI:and then the little bear said'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_quotation_precedes(self):
        actual_output = CHATCleaner.remove_terminator(
            '+” please give me all of your honey.')
        desired_output = 'please give me all of your honey.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_period_with_postcode_following(self):
        actual_output  = CHATCleaner.remove_terminator(
            'what did you. [+ neg]')
        desired_output = 'what did you [+ neg]'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_CA_begin_latch_with_postcode_following(self):
        actual_output  = CHATCleaner.remove_terminator(
            'what did you +=. [+ neg]')
        desired_output = 'what did you [+ neg]'
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_untranscribed_utterances-method.

    def test_untranscribed_utterances_xxx(self):
        actual_output = CHATCleaner.null_untranscribed_utterances('xxx')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_untranscribed_utterances_normal_utt(self):
        actual_output = CHATCleaner.null_untranscribed_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_event_utterances-method.

    def test_null_event_utterances_null(self):
        actual_output = CHATCleaner.null_event_utterances('0')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_normal_utt_event(self):
        actual_output = CHATCleaner.null_event_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_events-method.

    def test_remove_events_single_event(self):
        actual_output = CHATCleaner.remove_events(
            'Hey there &=coughs')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_multiple_events(self):
        actual_output = CHATCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes.')
        desired_output = 'I got cold.'
        self.assertEqual(actual_output, desired_output)

    # Tests for the handle_repetitions-method.

    def test_handle_repetitions_single_repetition(self):
        actual_output = CHATCleaner.handle_repetitions(
            "it's [x 4] like a um dog.")
        desired_output = "it's it's it's it's like a um dog."
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_multiple_repetitions(self):
        actual_output = CHATCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]')
        desired_output = 'Hey Hey there there there'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_omissions-method.

    def test_remove_omissions_single_omission(self):
        actual_output = CHATCleaner.remove_omissions(
            'where 0is my truck?')
        desired_output = 'where my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_multiple_omissions(self):
        actual_output = CHATCleaner.remove_omissions(
            'where 0is 0my truck?')
        desired_output = 'where truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_omission_with_marker(self):
        actual_output = CHATCleaner.remove_omissions(
            'where 0is [*] my truck?')
        desired_output = 'where my truck?'
        self.assertEqual(actual_output, desired_output)

    # Tests for the unify_untranscribed-method.

    def test_unify_untranscribed_untranscribed_xyz(self):
        actual_output = CHATCleaner.unify_untranscribed(
            'zzz xxx yyy truck?')
        desired_output = 'xxx xxx xxx truck?'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_form_markers-method.

    def test_remove_form_markers_l_marked(self):
        actual_output = CHATCleaner.remove_form_markers(
            "it's m@l a@l r@l k@l.")
        desired_output = "it's m a r k."
        self.assertEqual(actual_output, desired_output)

    def test_remove_form_markers_k_marked(self):
        actual_output = CHATCleaner.remove_form_markers(
            "it's mark@k.")
        desired_output = "it's mark."
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_linkers-method.

    def test_remove_linkers_quoted_utterance_linker_no_slash(self):
        actual_output = CHATCleaner.remove_linkers('+". where is  my truck?')
        desired_output = 'where my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers__quoted_utterance_linker_with_slash(self):
        actual_output = CHATCleaner.remove_linkers(
            '+"/. where is  my truck?')
        desired_output = 'where is  my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_quick_uptake_linker(self):
        actual_output = CHATCleaner.remove_linkers('+^ where is  my truck?')
        desired_output = 'where is  my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_lazy_overlap_marking_linker(self):
        actual_output = CHATCleaner.remove_linkers(
            '+< they had to go in here.')
        desired_output = 'they had to go in here.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_self_completion_linker(self):
        actual_output = CHATCleaner.remove_linkers('+, I go straight ahead.')
        desired_output = 'I go straight ahead.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_other_completion_linker(self):
        actual_output = CHATCleaner.remove_linkers('++ he would have come.')
        desired_output = 'he would have come.'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_separators-method.

    def test_remove_separators_comma_colon_semi(self):
        actual_output = CHATCleaner.remove_separators(
            'Hey there , what ; up : no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_ca-method.

    def test_remove_ca_falling_rising_mark(self):
        actual_output = CHATCleaner.remove_separators(
            'Hey there ↓ what up ↑ no ↓↑')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_marked_question(self):
        actual_output = CHATCleaner.remove_separators(
            'Hey there„ what up no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_question_rise_intonation_mark(self):
        actual_output = CHATCleaner.remove_separators(
            'Hey there ¿ what up no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_fillers-method.

    def test_remove_fillers(self):
        actual_output = CHATCleaner.remove_fillers('&-uh &-uh the water')
        desired_output = 'uh uh the water'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_pauses_within_words-method.

    def test_remove_pauses_within_words_one_pause(self):
        actual_output = CHATCleaner.remove_pauses_within_words('spa^ghetti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_multiple_pauses(self):
        actual_output = CHATCleaner.remove_pauses_within_words(
            'spa^ghe^tti bologne^se')
        desired_output = 'spaghetti bolognese'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_blocking-method. (≠ or ^)

    def test_remove_blocking(self):
        actual_output = CHATCleaner.remove_blocking(
            '≠hey ^there')
        desired_output = 'hey there'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_pauses_between_words-method.

    def test_remove_pauses_betwee_words(self):
        actual_output = CHATCleaner.remove_pauses_between_words(
            "I (.) don't (..) know (...) this.")
        desired_output = "I don't know this."
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_drawls-method.

    def test_remove_drawls_lengthened_syllable(self):
        actual_output = CHATCleaner.remove_drawls('bana:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_pause_between_syllables(self):
        actual_output = CHATCleaner.remove_drawls('rhi^noceros')
        desired_output = 'rhi^noceros'

    # Test for the remove_scoped_symbols-method.

    def test_remove_scoped_symbols(self):
        actual_output = CHATCleaner.remove_scoped_symbols(
            "<that's mine> [=! cries]")
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)
        # should the 'cries' remain in the string?


class TestInuktutCleaner(unittest.TestCase):
    """class to test the InuktutCleaner."""
    pass
    


if __name__ == '__main__':
    unittest.main()
