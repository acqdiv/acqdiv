import unittest
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner


class TestCHATUtteranceCleaner(unittest.TestCase):
    
    # Tests for the remove_redundant_whitespace-method.

    def test_remove_redundant_whitespace_leading_trailing_whitespace(self):
        """Test remove_redundant_whitespace with lead/end spaces."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            ' h ')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_whitespace(self):
        """Test remove_redundant_whitespace with multiple spaces."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '  h  h  ')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_tabs(self):
        """Test remove_redundant_whitespace with lead/end tabs."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\th\t')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_tabs(self):
        """Test remove_redundant_whitespace for multiple tabs."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\t\th\t\th\t\t')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_newlines(self):
        """Test remove_redundant_whitespace with lead/end newlines."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\nh\n')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_newlines(self):
        """Test remove_redundant_whitespace with multiple newlines."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\n\nh\n\nh\n\n')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_creturns(self):
        """remove_redundant_whitespace with lead/end carriage return."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\rh\r')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_creturns(self):
        """remove_redundant_whitespace with multiple carriage return."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\r\rh\r\rh\r\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_combinations(self):
        """Test remove_redundant_whitespace with mixed space chars."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces(
            '\n\t \r\r h   \nh \t\t\n\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_empty_string(self):
        """Test remove_redundant_whitespace with empty string."""
        actual_output = CHATUtteranceCleaner.remove_redundant_whitespaces('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_terminator-method.

    def test_remove_terminator_period(self):
        """Test remove_terminator with period."""
        actual_output = CHATUtteranceCleaner.remove_terminator('I got cold .')
        desired_output = 'I got cold'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_mark(self):
        """Test remove_terminator with question mark."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            'is that a carrot ?')
        desired_output = 'is that a carrot'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_exclamation_point(self):
        """Test remove_terminator with exclamation_point."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            'sit down !')
        desired_output = 'sit down'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_trailing_off(self):
        """Test remove_terminator with trailing off."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*SAR: smells good enough for +...')
        desired_output = '*SAR: smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_trailing_off_of_question(self):
        """Test remove_terminator with trailing off of a question."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*SAR: smells good enough for +..?')
        desired_output = '*SAR: smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_with_exclamation(self):
        """Test remove_terminator with question and exclamation(+!?)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?')
        desired_output = '*SAR: smells good enough for this'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption(self):
        """Test remove_terminator with interruption(+/.)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*MOT:what did you +/.')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption_of_a_question(self):
        """Test remove_terminator with interruption of question(+/?)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*MOT:what did you +/?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interruption(self):
        """Test remove_terminator with self interruption (+//.)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*SAR:smells good enough for +//.')
        desired_output = '*SAR:smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interrupted_question(self):
        """remove_terminator with self interrupted question (+//?)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*MOT:what did you +//?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_transcription_break(self):
        """Test remove_terminator with transcription break (+.)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*SAR:smells good enough for me +.')
        desired_output = '*SAR:smells good enough for me'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_CA_terminator(self):
        """Test remove_terminator with CA-Terminator (++.)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            'what did you ++.')
        desired_output = 'what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_quotation_follows(self):
        """Test remove_terminator with (+"/.)."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            '*CHI:and then the little bear said +"/.')
        desired_output = '*CHI:and then the little bear said'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_period_with_postcode_following(self):
        """Test remove_terminator with postcode at the end."""
        actual_output = CHATUtteranceCleaner.remove_terminator(
            'what did you. [+ neg]')
        desired_output = 'what did you [+ neg]'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_empty_string(self):
        """Test remove_terminator with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_terminator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_untranscribed_utterances-method.

    def test_null_untranscribed_utterances_standard_case(self):
        """Test null_untranscribed_utterances with '???'."""
        actual_output = CHATUtteranceCleaner.null_untranscribed_utterances(
            '???')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_utterances_normal_utt(self):
        """Test null_untranscribed_utterances with '???'."""
        actual_output = CHATUtteranceCleaner.null_untranscribed_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscibed_utterances_empty_string(self):
        """Test null_untranscribed_utterances with an empty string."""
        actual_output = CHATUtteranceCleaner.null_untranscribed_utterances('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_event_utterances-method.

    def test_null_event_utterances_null(self):
        """Test null_event_utterances with the string '0'"""
        actual_output = CHATUtteranceCleaner.null_event_utterances('0')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_and_other_words(self):
        """Test utterance containing other words apart from `0`."""
        actual_output = CHATUtteranceCleaner.null_event_utterances('0 true')
        desired_output = 'true'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_digit(self):
        """Test with zero digit."""
        actual_output = CHATUtteranceCleaner.null_event_utterances('10 years')
        desired_output = '10 years'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_terminator(self):
        """Test with null followed by terminator."""
        actual_output = CHATUtteranceCleaner.null_event_utterances('0.')
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_normal_utt(self):
        """Test null_event_utterances with a string without events."""
        actual_output = CHATUtteranceCleaner.null_event_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_empty_string(self):
        """Test null_event_utterances with an empty string"""
        actual_output = CHATUtteranceCleaner.null_event_utterances('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_events-method.

    def test_remove_events_single_event(self):
        """Test remove_events with an utt containing only one event."""
        actual_output = CHATUtteranceCleaner.remove_events(
            'Hey there &=coughs')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_multiple_events_with_space_before_terminator(self):
        """Test remove_events with an utt containing 3 events."""
        actual_output = CHATUtteranceCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes .')
        desired_output = 'I got cold .'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_events_multiple_events_'
                    'no_space_before_terminator skipped'))
    def test_remove_events_multiple_events_no_space_before_terminator(self):
        """Test remove_events with 3 events, no space before period."""
        actual_output = CHATUtteranceCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes.')
        desired_output = 'I got cold.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_empty_string(self):
        """Test remove_events with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_events('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the handle_repetitions-method.

    def test_handle_repetitions_single_repetition(self):
        """Test handle_repetitions with an utt containing 1 rep."""
        actual_output = CHATUtteranceCleaner.handle_repetitions(
            "it's [x 4] like a um dog.")
        desired_output = "it's it's it's it's like a um dog."
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_multiple_repetitions(self):
        """Test handle_repetitions with an utt containing 2 reps."""
        actual_output = CHATUtteranceCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]')
        desired_output = 'Hey Hey there there there'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_scope_over_three_words(self):
        """Test handle_repetitions with a scope of 3 words."""
        actual_output = CHATUtteranceCleaner.handle_repetitions(
            '<how are you> [x 2]')
        desired_output = 'how are you how are you'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_non_scope_angle_bracket(self):
        """Test with a non-scope angle bracket `[<]`."""
        utterance = 'ha [<] <ho ho> [x 2]'
        actual_output = CHATUtteranceCleaner.handle_repetitions(utterance)
        desired_output = 'ha [<] ho ho ho ho'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_empty_string(self):
        """Test handle_repetitions with an empty string."""
        actual_output = CHATUtteranceCleaner.handle_repetitions('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_no_whitespace(self):
        """Test handle_repetitions with missing whitespace."""
        actual_output = CHATUtteranceCleaner.handle_repetitions('hello[x 2]')
        desired_output = 'hello hello'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_scoped_symbol_before(self):
        """Test with a preceding scoped symbol."""
        utterance = 'hey@i [=! screams] [x 2] .'
        actual_output = CHATUtteranceCleaner.handle_repetitions(utterance)
        desired_output = 'hey@i [=! screams] hey@i [=! screams] .'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_10_repetitions(self):
        """Test with 10 repetitions."""
        actual_output = CHATUtteranceCleaner.handle_repetitions('a [x 10]')
        desired_output = 'a a a a a a a a a a'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_omissions-method.

    def test_remove_omissions_single_omission(self):
        """Test remove_omissions with an utt containing 1 omission."""
        actual_output = CHATUtteranceCleaner.remove_omissions(
            'where 0is my truck?')
        desired_output = 'where my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_multiple_omissions_space_before_terminator(self):
        """Test remove_omissions with an utt containing 3 omissions."""
        actual_output = CHATUtteranceCleaner.remove_omissions(
            '0but where 0is my 0truck ?')
        desired_output = 'where my ?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_omission_in_brackets(self):
        """Test remove_omissions with omission in square brackets."""
        utterance = 'This [* 0is] what ?'
        actual_output = CHATUtteranceCleaner.remove_omissions(utterance)
        desired_output = 'This [* 0is] what ?'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_omissions_multiple_omissions_'
                    'no_space_before_terminator skipping'))
    def test_remove_omissions_multiple_omissions_no_space_before_terminator(
            self):
        """Test with 3 omissions and no space before terminator."""
        actual_output = CHATUtteranceCleaner.remove_omissions(
            '0but where 0is my 0truck?')
        desired_output = 'where my?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_empty_string(self):
        """Test remove_omissions with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_omissions('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_null_utterance_no_whitespace(self):
        """Test with null utterance and no whitespace."""
        utterance = '0[=! applauses]'
        actual_output = CHATUtteranceCleaner.remove_omissions(utterance)
        desired_output = '0[=! applauses]'
        self.assertEqual(actual_output, desired_output)

    # Tests for the unify_untranscribed-method.

    def test_unify_untranscribed_xyw(self):
        """Test unify_untranscribed with 'xxx', 'yyy' and 'www'."""
        actual_output = CHATUtteranceCleaner.unify_untranscribed(
            'www xxx truck yyy ?')
        desired_output = '??? ??? truck ??? ?'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_untranscribed_empty_string(self):
        """Test unify_untranscribed with an empty string."""
        actual_output = CHATUtteranceCleaner.unify_untranscribed('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_linkers-method.

    def test_remove_linkers_quoted_utterance_linker_no_slash(self):
        """Test remove_linkers with quoted utterance linker (+")."""
        actual_output = CHATUtteranceCleaner.remove_linkers(
            '+" where is my truck?')
        desired_output = 'where is my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_quick_uptake_linker(self):
        """Test remove_linkers with quick uptake linker (+^)."""
        actual_output = CHATUtteranceCleaner.remove_linkers(
            '+^ where is  my truck?')
        desired_output = 'where is  my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_lazy_overlap_marking_linker(self):
        """Test remove_linkers with lazy overlap linker (+<)."""
        actual_output = CHATUtteranceCleaner.remove_linkers(
            '+< they had to go in here.')
        desired_output = 'they had to go in here.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_self_completion_linker(self):
        """Test remove_linkers with self completion linker (+,)."""
        actual_output = CHATUtteranceCleaner.remove_linkers(
            '+, I go straight ahead.')
        desired_output = 'I go straight ahead.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_other_completion_linker(self):
        """Test remove_linkers with self completion linker (+,)."""
        actual_output = CHATUtteranceCleaner.remove_linkers(
            '++ he would have come.')
        desired_output = 'he would have come.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_empty_string(self):
        """Test remove_linkers with empty string."""
        actual_output = CHATUtteranceCleaner.remove_linkers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_separators-method.

    def test_remove_separators_comma_colon_semi(self):
        """Test remove_separators with comma, colon and semicolon."""
        actual_output = CHATUtteranceCleaner.remove_separators(
            'Hey there , what ; up : no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_separators_empty_string(self):
        """Test remove_separators with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_separators('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_ca-method.

    def test_remove_ca_quotations(self):
        """Test remove_ca with opening and closing quotations."""
        actual_output = CHATUtteranceCleaner.remove_ca(
            '“Hey there what up no”')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_falling_rising_mark(self):
        """Test remove_ca with 3 rising (↑) and 1 falling (↓) mark."""
        actual_output = CHATUtteranceCleaner.remove_ca(
            'Hey↑ there↓ what up↑ no↑')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_marked_question(self):
        """Test remove_ca with marked question („)."""
        actual_output = CHATUtteranceCleaner.remove_ca(
            'Hey there„ what up no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_satellite_marker(self):
        """Test remove_ca with satellite marker (‡)."""
        actual_output = CHATUtteranceCleaner.remove_ca(
            'no ‡ Mommy no go')
        desired_output = 'no Mommy no go'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_empty_string(self):
        """Test remove_ca with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_ca('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_pauses_between_words-method.

    def test_remove_pauses_between_words_multiple_pauses(self):
        """Test remove_pauses with 3 pauses of different length."""
        actual_output = CHATUtteranceCleaner.remove_pauses_between_words(
            "I (.) don't (..) know (...) this.")
        desired_output = "I don't know this."
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_between_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_pauses_between_words('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_scoped_symbols-method.

    def test_remove_scoped_symbols_not_nested(self):
        """Test remove_scoped_symbols with 2 not nested symbol pairs."""
        utterance = "<that's mine> [=! cries]"
        actual_output = CHATUtteranceCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_one_level_nested(self):
        """Test remove_scoped_symbols with 1 level of nestedness."""
        utterance = "<that's mine [=! cries]>"
        actual_output = CHATUtteranceCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_two_levels_nested(self):
        """Test remove_scoped_symbols with 2 levels of nestedness."""
        utterance = "<that's mine <she said [=! cries]>> [=! slaps leg]"
        actual_output = CHATUtteranceCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine she said"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_empty_string(self):
        """Test remove_scoped_symbols with an empty string."""
        actual_output = CHATUtteranceCleaner.remove_scoped_symbols('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_no_withespace(self):
        """Test remove_scoped_symbols with missing whitespace."""
        utterance = '0[=! just testing something]'
        actual_output = CHATUtteranceCleaner.remove_scoped_symbols(utterance)
        desired_output = '0'
        self.assertEqual(actual_output, desired_output)
