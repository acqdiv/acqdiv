import unittest
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.YucatecCleaner import YucatecCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    Class to test the CHATCleaner.

    A lot of the test cases are taken from or inspired by
    https://talkbank.org/manuals/CHAT.pdf
    .
    """

    # ---------- metadata cleaning ----------

    def test_clean_date_regular_date(self):
        """Test clean_date with a regular date as input."""
        actual_output = CHATCleaner.clean_date('12-SEP-1997')
        desired_output = '1997-09-12'
        self.assertEqual(actual_output, desired_output)

    def test_clean_date_empty_string(self):
        """Test clean_date with empty string as input."""
        actual_output = CHATCleaner.clean_date('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test utterance cleaning ----------

    # Tests for the remove_redundant_whitespace-method.

    def test_remove_redundant_whitespace_leading_trailing_whitespace(self):
        """Test remove_redundant_whitespace with lead/end spaces."""
        actual_output = CHATCleaner.remove_redundant_whitespaces(' h ')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_whitespace(self):
        """Test remove_redundant_whitespace with multiple spaces."""
        actual_output = CHATCleaner.remove_redundant_whitespaces('  h  h  ')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_tabs(self):
        """Test remove_redundant_whitespace with lead/end tabs."""
        actual_output = CHATCleaner.remove_redundant_whitespaces('\th\t')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_tabs(self):
        """Test remove_redundant_whitespace for multiple tabs."""
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\t\th\t\th\t\t')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_newlines(self):
        """Test remove_redundant_whitespace with lead/end newlines."""
        actual_output = CHATCleaner.remove_redundant_whitespaces('\nh\n')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_newlines(self):
        """Test remove_redundant_whitespace with multiple newlines."""
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\n\nh\n\nh\n\n')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_leading_trailing_creturns(self):
        """remove_redundant_whitespace with lead/end carriage return."""
        actual_output = CHATCleaner.remove_redundant_whitespaces('\rh\r')
        desired_output = 'h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_multiple_creturns(self):
        """remove_redundant_whitespace with multiple carriage return."""
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\r\rh\r\rh\r\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_combinations(self):
        """Test remove_redundant_whitespace with mixed space chars."""
        actual_output = CHATCleaner.remove_redundant_whitespaces(
            '\n\t \r\r h   \nh \t\t\n\r')
        desired_output = 'h h'
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespace_empty_string(self):
        """Test remove_redundant_whitespace with empty string."""
        actual_output = CHATCleaner.remove_redundant_whitespaces('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_terminator-method.

    def test_remove_terminator_period(self):
        """Test remove_terminator with period."""
        actual_output = CHATCleaner.remove_terminator('I got cold .')
        desired_output = 'I got cold'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_mark(self):
        """Test remove_terminator with question mark."""
        actual_output = CHATCleaner.remove_terminator(
            'is that a carrot ?')
        desired_output = 'is that a carrot'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_exclamation_point(self):
        """Test remove_terminator with exclamation_point."""
        actual_output = CHATCleaner.remove_terminator(
            'sit down !')
        desired_output = 'sit down'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_trailing_off(self):
        """Test remove_terminator with trailing off."""
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +...')
        desired_output = '*SAR: smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_trailing_off_of_question(self):
        """Test remove_terminator with trailing off of a question."""
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +..?')
        desired_output = '*SAR: smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_question_with_exclamation(self):
        """Test remove_terminator with question and exclamation(+!?)."""
        actual_output = CHATCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?')
        desired_output = '*SAR: smells good enough for this'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption(self):
        """Test remove_terminator with interruption(+/.)."""
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +/.')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_interruption_of_a_question(self):
        """Test remove_terminator with interruption of question(+/?)."""
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +/?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interruption(self):
        """Test remove_terminator with self interruption (+//.)."""
        actual_output = CHATCleaner.remove_terminator(
            '*SAR:smells good enough for +//.')
        desired_output = '*SAR:smells good enough for'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_self_interrupted_question(self):
        """remove_terminator with self interrupted question (+//?)."""
        actual_output = CHATCleaner.remove_terminator(
            '*MOT:what did you +//?')
        desired_output = '*MOT:what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_transcription_break(self):
        """Test remove_terminator with transcription break (+.)."""
        actual_output = CHATCleaner.remove_terminator(
            '*SAR:smells good enough for me +.')
        desired_output = '*SAR:smells good enough for me'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_CA_terminator(self):
        """Test remove_terminator with CA-Terminator (++.)."""
        actual_output = CHATCleaner.remove_terminator(
            'what did you ++.')
        desired_output = 'what did you'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_quotation_follows(self):
        """Test remove_terminator with (+"/.)."""
        actual_output = CHATCleaner.remove_terminator(
            '*CHI:and then the little bear said +"/.')
        desired_output = '*CHI:and then the little bear said'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_period_with_postcode_following(self):
        """Test remove_terminator with postcode at the end."""
        actual_output = CHATCleaner.remove_terminator(
            'what did you. [+ neg]')
        desired_output = 'what did you [+ neg]'
        self.assertEqual(actual_output, desired_output)

    def test_remove_terminator_empty_string(self):
        """Test remove_terminator with an empty string."""
        actual_output = CHATCleaner.remove_terminator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_untranscribed_utterances-method.

    def test_null_untranscribed_utterances_standard_case(self):
        """Test null_untranscribed_utterances with '???'."""
        actual_output = CHATCleaner.null_untranscribed_utterances('???')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_utterances_normal_utt(self):
        """Test null_untranscribed_utterances with '???'."""
        actual_output = CHATCleaner.null_untranscribed_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscibed_utterances_empty_string(self):
        """Test null_untranscribed_utterances with an empty string."""
        actual_output = CHATCleaner.null_untranscribed_utterances('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_event_utterances-method.

    def test_null_event_utterances_null(self):
        """Test null_event_utterances with the string '0'"""
        actual_output = CHATCleaner.null_event_utterances('0')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_and_other_words(self):
        """Test utterance containing other words apart from `0`."""
        actual_output = CHATCleaner.null_event_utterances('0 true')
        desired_output = 'true'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_digit(self):
        """Test with zero digit."""
        actual_output = CHATCleaner.null_event_utterances('10 years')
        desired_output = '10 years'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_null_terminator(self):
        """Test with null followed by terminator."""
        actual_output = CHATCleaner.null_event_utterances('0.')
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_normal_utt(self):
        """Test null_event_utterances with a string without events."""
        actual_output = CHATCleaner.null_event_utterances(
            'Hey there')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_null_event_utterances_empty_string(self):
        """Test null_event_utterances with an empty string"""
        actual_output = CHATCleaner.null_event_utterances('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_events-method.

    def test_remove_events_single_event(self):
        """Test remove_events with an utt containing only one event."""
        actual_output = CHATCleaner.remove_events(
            'Hey there &=coughs')
        desired_output = 'Hey there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_multiple_events_with_space_before_terminator(self):
        """Test remove_events with an utt containing 3 events."""
        actual_output = CHATCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes .')
        desired_output = 'I got cold .'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_events_multiple_events_'
                    'no_space_before_terminator skipped'))
    def test_remove_events_multiple_events_no_space_before_terminator(self):
        """Test remove_events with 3 events, no space before period."""
        actual_output = CHATCleaner.remove_events(
            '&=gasps I got &=groans cold &=vocalizes.')
        desired_output = 'I got cold.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_events_empty_string(self):
        """Test remove_events with an empty string."""
        actual_output = CHATCleaner.remove_events('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the handle_repetitions-method.

    def test_handle_repetitions_single_repetition(self):
        """Test handle_repetitions with an utt containing 1 rep."""
        actual_output = CHATCleaner.handle_repetitions(
            "it's [x 4] like a um dog.")
        desired_output = "it's it's it's it's like a um dog."
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_multiple_repetitions(self):
        """Test handle_repetitions with an utt containing 2 reps."""
        actual_output = CHATCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]')
        desired_output = 'Hey Hey there there there'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_scope_over_three_words(self):
        """Test handle_repetitions with a scope of 3 words."""
        actual_output = CHATCleaner.handle_repetitions(
            '<how are you> [x 2]')
        desired_output = 'how are you how are you'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_non_scope_angle_bracket(self):
        """Test with a non-scope angle bracket `[<]`."""
        utterance = 'ha [<] <ho ho> [x 2]'
        actual_output = CHATCleaner.handle_repetitions(utterance)
        desired_output = 'ha [<] ho ho ho ho'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_empty_string(self):
        """Test handle_repetitions with an empty string."""
        actual_output = CHATCleaner.handle_repetitions('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_no_whitespace(self):
        """Test handle_repetitions with missing whitespace."""
        actual_output = CHATCleaner.handle_repetitions('hello[x 2]')
        desired_output = 'hello hello'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_scoped_symbol_before(self):
        """Test with a preceding scoped symbol."""
        utterance = 'hey@i [=! screams] [x 2] .'
        actual_output = CHATCleaner.handle_repetitions(utterance)
        desired_output = 'hey@i [=! screams] hey@i [=! screams] .'
        self.assertEqual(actual_output, desired_output)

    def test_handle_repetitions_10_repetitions(self):
        """Test with 10 repetitions."""
        actual_output = CHATCleaner.handle_repetitions('a [x 10]')
        desired_output = 'a a a a a a a a a a'
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_omissions-method.

    def test_remove_omissions_single_omission(self):
        """Test remove_omissions with an utt containing 1 omission."""
        actual_output = CHATCleaner.remove_omissions(
            'where 0is my truck?')
        desired_output = 'where my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_multiple_omissions_space_before_terminator(self):
        """Test remove_omissions with an utt containing 3 omissions."""
        actual_output = CHATCleaner.remove_omissions(
            '0but where 0is my 0truck ?')
        desired_output = 'where my ?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_omission_in_brackets(self):
        """Test remove_omissions with omission in square brackets."""
        utterance = 'This [* 0is] what ?'
        actual_output = CHATCleaner.remove_omissions(utterance)
        desired_output = 'This [* 0is] what ?'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_omissions_multiple_omissions_'
                    'no_space_before_terminator skipping'))
    def test_remove_omissions_multiple_omissions_no_space_before_terminator(
            self):
        """Test with 3 omissions and no space before terminator."""
        actual_output = CHATCleaner.remove_omissions(
            '0but where 0is my 0truck?')
        desired_output = 'where my?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_empty_string(self):
        """Test remove_omissions with an empty string."""
        actual_output = CHATCleaner.remove_omissions('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_omissions_null_utterance_no_whitespace(self):
        """Test with null utterance and no whitespace."""
        utterance = '0[=! applauses]'
        actual_output = CHATCleaner.remove_omissions(utterance)
        desired_output = '0[=! applauses]'
        self.assertEqual(actual_output, desired_output)

    # Tests for the unify_untranscribed-method.

    def test_unify_untranscribed_xyw(self):
        """Test unify_untranscribed with 'xxx', 'yyy' and 'www'."""
        actual_output = CHATCleaner.unify_untranscribed(
            'www xxx truck yyy ?')
        desired_output = '??? ??? truck ??? ?'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_untranscribed_empty_string(self):
        """Test unify_untranscribed with an empty string."""
        actual_output = CHATCleaner.unify_untranscribed('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_form_markers_empty_string(self):
        """Test remove_form_markers with empty string."""
        actual_output = CHATCleaner.remove_form_markers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_linkers-method.

    def test_remove_linkers_quoted_utterance_linker_no_slash(self):
        """Test remove_linkers with quoted utterance linker (+")."""
        actual_output = CHATCleaner.remove_linkers('+" where is my truck?')
        desired_output = 'where is my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_quick_uptake_linker(self):
        """Test remove_linkers with quick uptake linker (+^)."""
        actual_output = CHATCleaner.remove_linkers('+^ where is  my truck?')
        desired_output = 'where is  my truck?'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_lazy_overlap_marking_linker(self):
        """Test remove_linkers with lazy overlap linker (+<)."""
        actual_output = CHATCleaner.remove_linkers(
            '+< they had to go in here.')
        desired_output = 'they had to go in here.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_self_completion_linker(self):
        """Test remove_linkers with self completion linker (+,)."""
        actual_output = CHATCleaner.remove_linkers('+, I go straight ahead.')
        desired_output = 'I go straight ahead.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_other_completion_linker(self):
        """Test remove_linkers with self completion linker (+,)."""
        actual_output = CHATCleaner.remove_linkers('++ he would have come.')
        desired_output = 'he would have come.'
        self.assertEqual(actual_output, desired_output)

    def test_remove_linkers_empty_string(self):
        """Test remove_linkers with empty string."""
        actual_output = CHATCleaner.remove_linkers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_separators-method.

    def test_remove_separators_comma_colon_semi(self):
        """Test remove_separators with comma, colon and semicolon."""
        actual_output = CHATCleaner.remove_separators(
            'Hey there , what ; up : no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_separators_empty_string(self):
        """Test remove_separators with an empty string."""
        actual_output = CHATCleaner.remove_separators('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_ca-method.

    def test_remove_ca_quotations(self):
        """Test remove_ca with opening and closing quotations."""
        actual_output = CHATCleaner.remove_ca(
            '“Hey there what up no”')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_falling_rising_mark(self):
        """Test remove_ca with 3 rising (↑) and 1 falling (↓) mark."""
        actual_output = CHATCleaner.remove_ca(
            'Hey↑ there↓ what up↑ no↑')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_marked_question(self):
        """Test remove_ca with marked question („)."""
        actual_output = CHATCleaner.remove_ca(
            'Hey there„ what up no')
        desired_output = 'Hey there what up no'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_satellite_marker(self):
        """Test remove_ca with satellite marker (‡)."""
        actual_output = CHATCleaner.remove_ca(
            'no ‡ Mommy no go')
        desired_output = 'no Mommy no go'
        self.assertEqual(actual_output, desired_output)

    def test_remove_ca_empty_string(self):
        """Test remove_ca with an empty string."""
        actual_output = CHATCleaner.remove_ca('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_pauses_between_words-method.

    def test_remove_pauses_between_words_multiple_pauses(self):
        """Test remove_pauses with 3 pauses of different length."""
        actual_output = CHATCleaner.remove_pauses_between_words(
            "I (.) don't (..) know (...) this.")
        desired_output = "I don't know this."
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_between_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = CHATCleaner.remove_pauses_between_words('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_scoped_symbols-method.

    def test_remove_scoped_symbols_not_nested(self):
        """Test remove_scoped_symbols with 2 not nested symbol pairs."""
        utterance = "<that's mine> [=! cries]"
        actual_output = CHATCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_one_level_nested(self):
        """Test remove_scoped_symbols with 1 level of nestedness."""
        utterance = "<that's mine [=! cries]>"
        actual_output = CHATCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_two_levels_nested(self):
        """Test remove_scoped_symbols with 2 levels of nestedness."""
        utterance = "<that's mine <she said [=! cries]>> [=! slaps leg]"
        actual_output = CHATCleaner.remove_scoped_symbols(utterance)
        desired_output = "that's mine she said"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_empty_string(self):
        """Test remove_scoped_symbols with an empty string."""
        actual_output = CHATCleaner.remove_scoped_symbols('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_no_withespace(self):
        """Test remove_scoped_symbols with missing whitespace."""
        utterance = '0[=! just testing something]'
        actual_output = CHATCleaner.remove_scoped_symbols(utterance)
        desired_output = '0'
        self.assertEqual(actual_output, desired_output)

    # Tests for the clean_utterance-method.

    def test_clean_utterance_clean_utt(self):
        """Test remove utterance using with already clean utterance."""
        utterance = "that's mine she said"
        actual_output = CHATCleaner.clean_utterance(utterance)
        desired_output = "that's mine she said"
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_mixed_things_to_clean(self):
        """Test all utterance cleaning methods at once.

        The utterance contains:
        - redundant whitespace
        - terminator
        - untranscribed
        - events
        - Null-event
        - repetition
        - scoped symbols
        - pause between words
        """
        utterance = ("+^ that's [x 2] xxx (..) mine ↓ &=vocalizes ; <0you"
                     " pig <she said   [=! cries]>> [=! slaps leg] +/.")
        actual_output = CHATCleaner.clean_utterance(utterance)
        desired_output = "that's that's ??? mine pig she said"
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        """Test clean_utterance with an empty string."""
        utterance = ''
        actual_output = CHATCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_null(self):
        """Test with null utterance."""
        utterance = '0[=! applauses]'
        actual_output = CHATCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test word cleaning ----------

    # Tests for the remove_form_markers-method.

    def test_remove_form_markers_l_marked_one_char_length(self):
        """Test remove_form_markers with marks of one char length."""
        word = 'mark@l'
        actual_output = CHATCleaner.remove_form_markers(
            word)
        desired_output = "mark"
        self.assertEqual(actual_output, desired_output)

    def test_remove_form_markers_si_marked_two_char_length(self):
        """Test remove_form_markers with mark of two chars length."""
        actual_output = CHATCleaner.remove_form_markers(
            'mark@si')
        desired_output = 'mark'
        self.assertEqual(actual_output, desired_output)

    @unittest.skip(('test_remove_form_markers_mixed_'
                    'no_space_before_terminator skipping'))
    def test_remove_form_markers_mixed_no_space_before_terminator(self):
        """Test remove_form_markers with 1 '@k' and one '@l' mark.

        No space between mark and terminator.
        """
        actual_output = CHATCleaner.remove_form_markers(
            "mark@k.")
        desired_output = "mark."
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_drawls-method.

    def test_remove_drawls_single_lengthened_syllable(self):
        """Test remove_drawls with 1 lengthened syllable (:)."""
        actual_output = CHATCleaner.remove_drawls('bana:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_multiple_lengthened_syllables(self):
        """Test remove_drawls with 2 lengthened syllables (:)."""
        actual_output = CHATCleaner.remove_drawls('ba:na:nas')
        desired_output = 'bananas'
        self.assertEqual(actual_output, desired_output)

    def test_remove_drawls_empty_string(self):
        """Test remove_drawls with an empty string."""
        actual_output = CHATCleaner.remove_drawls('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_pauses_within_words-method.

    def test_remove_pauses_within_words_one_pause(self):
        """Test remove_pauses with 1 pause (^)."""
        actual_output = CHATCleaner.remove_pauses_within_words(
            'spa^ghetti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_multiple_pauses(self):
        """Test remove_pauses with 2 pauses (^)."""
        actual_output = CHATCleaner.remove_pauses_within_words(
            'spa^ghe^tti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_two_pauses_one_letter_in_between(self):
        """Test remove_pauses with two pauses separated by one letter."""
        actual_output = CHATCleaner.remove_pauses_within_words('m^a^t')
        desired_output = 'mat'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_pause_at_the_end(self):
        """Test remove_pauses with one pause at the end."""
        actual_output = CHATCleaner.remove_pauses_within_words('ma^')
        desired_output = 'ma'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = CHATCleaner.remove_pauses_within_words('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_blocking(self):
        """Test remove_pauses with blocking."""
        actual_output = CHATCleaner.remove_pauses_within_words('^hey')
        desired_output = '^hey'
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_blocking-method. (≠ or ^)

    def test_remove_blocking_unequal_sign(self):
        """Test remove_blocking with an unequal sign as marker (≠)."""
        actual_output = CHATCleaner.remove_blocking(
            '≠hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_circumflex(self):
        """Test remove_blocking with a circumflex as marker (^)."""
        actual_output = CHATCleaner.remove_blocking(
            '^there')
        desired_output = 'there'
        self.assertEqual(actual_output, desired_output)

    def test_remove_blocking_empty_string(self):
        """Test remove_blocking with an empty string."""
        actual_output = CHATCleaner.remove_blocking('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_fillers-method.

    def test_remove_filler_without_dash(self):
        """Test remove_filler without dash."""
        word = '&hu'
        actual_output = CHATCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_with_dash(self):
        """Test remove_fillers with dash."""
        word = '&-hu'
        actual_output = CHATCleaner.remove_filler(word)
        desired_output = 'hu'
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_empty_string(self):
        """Test remove_fillers with 3 fillers (&-uh)."""
        word = ''
        actual_output = CHATCleaner.remove_filler(word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_filler_ampersand_with_equal_sign(self):
        """Test remove_fillers with ampersand and equal sign."""
        word = '&=hu'
        actual_output = CHATCleaner.remove_filler(word)
        desired_output = '&=hu'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_already_clean(self):
        """Test clean_word with an already clean word."""
        actual_output = CHATCleaner.clean_word('ka')
        desired_output = 'ka'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_mixed(self):
        """Test clean_word with markers, drawls, pauses and blocking."""
        actual_output = CHATCleaner.clean_word('^ka:l^e@e')
        desired_output = 'kale'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_empty_string(self):
        """Test clean_word with an empty string."""
        actual_output = CHATCleaner.clean_word('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- test morphology tier cleaning ----------

    def test_clean_seg_tier(self):
        """Test clean_seg_tier for same input as output."""
        seg_tier = 'ha be'
        actual_output = CHATCleaner.clean_seg_tier(seg_tier)
        desired_output = seg_tier
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier for same input as output."""
        gloss_tier = 'ha be'
        actual_output = CHATCleaner.clean_gloss_tier(gloss_tier)
        desired_output = gloss_tier
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier for same input as output."""
        pos_tier = 'ha be'
        actual_output = CHATCleaner.clean_pos_tier(pos_tier)
        desired_output = pos_tier
        self.assertEqual(actual_output, desired_output)

    # ---------- cross cleaning ---------

    def test_utterance_cross_clean(self):
        """Test utterance_cross_clean for same input as output."""
        raw_utt = ''
        actual_utt = 'ha be'
        target_utt = 'ha be'
        seg_tier = 'h_a b_e'
        gloss_tier = '1sg pl'
        pos_tier = 'V N'
        actual_output = CHATCleaner.utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier)
        desired_output = (actual_utt, target_utt, seg_tier, gloss_tier,
                          pos_tier)
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme word cleaning ----------

    def test_clean_seg_word(self):
        """Test clean_seg_word, same input as output."""
        seg_word = 'ke'
        actual_output = CHATCleaner.clean_seg_word(seg_word)
        desired_output = seg_word
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_word(self):
        """Test clean_gloss_word, same input as output."""
        gloss_word = 'wh'
        actual_output = CHATCleaner.clean_gloss_word(gloss_word)
        desired_output = gloss_word
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_word(self):
        """Test clean_pos_word, same input as output."""
        pos_word = 'V'
        actual_output = CHATCleaner.clean_pos_word(pos_word)
        desired_output = pos_word
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme cleaning ----------

    def test_clean_segment(self):
        """Test clean_segment, same input as output."""
        segment = 'he'
        actual_output = CHATCleaner.clean_segment(segment)
        desired_output = segment
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        """Test clean_gloss, same input as output."""
        gloss = 'he'
        actual_output = CHATCleaner.clean_gloss(gloss)
        desired_output = gloss
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos(self):
        """Test clean_pos, same input as output."""
        pos = 'he'
        actual_output = CHATCleaner.clean_pos(pos)
        desired_output = pos
        self.assertEqual(actual_output, desired_output)


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

###############################################################################


if __name__ == '__main__':
    unittest.main()
