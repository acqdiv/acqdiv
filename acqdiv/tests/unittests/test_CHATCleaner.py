import unittest
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.InuktitutCleaner import InuktitutCleaner
from acqdiv.parsers.chat.cleaners.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner
from acqdiv.parsers.chat.cleaners.SesothoCleaner import SesothoCleaner
from acqdiv.parsers.chat.cleaners.TurkishCleaner import TurkishCleaner
from acqdiv.parsers.chat.cleaners.YucatecCleaner import YucatecCleaner
from acqdiv.parsers.chat.cleaners.NungonCleaner import NungonCleaner


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


###############################################################################

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


###############################################################################


###############################################################################

class TestJapaneseMiiProCleaner(unittest.TestCase):
    """Class to test the JapaneseMiiProCleaner."""

    cleaner = JapaneseMiiProCleaner()

    def test_remove_non_words_single(self):
        """Test remove_non_words with 1 non-word on the morphtier."""
        morph_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_multiple(self):
        """Test remove_non_words with 3 non-words on the morphtier."""
        morph_tier = 'tag|V n:prop|Ikun tag|do tag|‡ .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_no_non_words(self):
        """Test remove_non_words with no non-words on the morphtier."""
        morph_tier = 'n:prop|Ikun .'
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = 'n:prop|Ikun .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_non_words_empty_string(self):
        """Test remove_non_words with an empty string."""
        morph_tier = ''
        actual_output = JapaneseMiiProCleaner.remove_non_words(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_single(self):
        """Test clean_morph_tier with 1 non-word and period."""
        morph_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_multiple(self):
        """Test clean_morph_tier with 3 non-words and question mark."""
        morph_tier = 'tag|da tag|do n:prop|Ikun tag|‡ ?'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_no_non_words(self):
        """Test clean_morph_tier with no non-words and excl mark."""
        morph_tier = 'n:prop|Ikun !'
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_empty_string(self):
        """Test clean_morph_tier with no non-words and excl mark."""
        morph_tier = ''
        actual_output = JapaneseMiiProCleaner.clean_morph_tier(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        """Test clean_seg_tier with 1 non-word.

        Since clean_seg_tier only calls clean_morph_tier and this method
        is already tested above, only one test to test the general
        functionality is used.
        """
        seg_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_seg_tier(seg_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        """Test clean_gloss_tier with 1 non-word.

        Since clean_gloss_tier only calls clean_morph_tier and this
        method is already tested above, only one test to test the
        general functionality is used.
        """
        gloss_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        """Test clean_pos_tier with 1 non-word.

        Since clean_pos_tier only calls clean_morph_tier and this
        method is already tested above, only one test to test the
        general functionality is used.
        """
        pos_tier = 'n:prop|Ikun tag|‡ .'
        actual_output = JapaneseMiiProCleaner.clean_pos_tier(pos_tier)
        desired_output = 'n:prop|Ikun'
        self.assertEqual(actual_output, desired_output)

    # ---------- add_repetitions ----------

    def test_add_repetitions_aligned_no_scoping(self):
        raw_utterance = 'huhu repeat [x 2] hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_aligned_scoping(self):
        raw_utterance = 'huhu <ha ho> [x 2] hihi'
        morph_tier = 'N|huhu N|ha N|ho N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|ha N|ho N|ha N|ho N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_aligned_complicated_utt(self):
        raw_utterance = '+^ huhu [x 2] xxx [= not know] (..) ; haha [: höhö]'
        morph_tier = 'N|huhu N|xxx N|haha'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|huhu N|xxx N|haha'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_misaligned(self):
        raw_utterance = 'huhu repeat [x 2] hihi'
        morph_tier = 'N|huhu N|repeat N|hihi N|hö'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|repeat N|hihi N|hö'
        self.assertEqual(actual_output, desired_output)

    def test_add_repetitions_no_reps(self):
        raw_utterance = 'huhu haha hihi'
        morph_tier = 'N|huhu N|haha N|hihi'
        actual_output = JapaneseMiiProCleaner.add_repetitions(
            raw_utterance, morph_tier)
        desired_output = 'N|huhu N|haha N|hihi'
        self.assertEqual(actual_output, desired_output)

    # ---------- add retracings ----------

    def test_add_retracings_aligned_no_scoping(self):
        raw_utt = 'huhu repeat [/] repeat hihi'
        actual_utt = 'huhu repeat repeat hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_aligned_scoping(self):
        raw_utt = 'tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'tutu ha ho ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_misaligned1(self):
        raw_utt = 'tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'tutu ha ho ha ho kuku'
        morph_tier = 'N|bubu N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|bubu N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_misaligned2(self):
        raw_utt = 'bubu tutu <ha ho> [/] ha ho kuku'
        actual_utt = 'bubu tutu ha ho ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_no_retracing(self):
        raw_utt = 'tutu ha ho kuku'
        actual_utt = 'tutu ha ho kuku'
        morph_tier = 'N|tutu N|ha N|ho N|kuku'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|tutu N|ha N|ho N|kuku'
        self.assertEqual(actual_output, desired_output)

    def test_add_retracings_unclean_actual_words(self):
        raw_utt = 'huhu repeat@o [/] repeat hihi'
        actual_utt = 'huhu repeat@o repeat hihi'
        morph_tier = 'N|huhu N|repeat N|hihi'
        actual_output = JapaneseMiiProCleaner.add_retracings(
            raw_utt, actual_utt, morph_tier)
        desired_output = 'N|huhu N|repeat N|repeat N|hihi'
        self.assertEqual(actual_output, desired_output)


###############################################################################


class TestSesothoCleaner(unittest.TestCase):

    # ---------- utterance cleaning ----------

    def test_clean_utterance_parenthesized_words(self):
        """Test clean_utterance with parenthesized words.

        Two words entirely surrounded by parentheses and two words
        partly surrounded by parentheses.
        """
        utterance = '(ho)dula tsamaya  (ho)dula (uye) ausi (uye) .'
        actual_output = SesothoCleaner.clean_utterance(utterance)
        desired_output = 'hodula tsamaya hodula ausi'
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        """Test clean_utterance with empty string."""
        utterance = ''
        actual_output = SesothoCleaner.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_single_beginning(self):
        """Test remove_words_parentheses with 1 parenth. word at beginning."""
        utterance = '(uye) ausi .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_single_end(self):
        """Test remove_words_parentheses with 1 parenth. word at end."""
        utterance = 'ausi (uye) .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_multiple(self):
        """Test remove_words_parentheses with 3 word in parentheses."""
        utterance = '(uye) ausi (uye) (uye) .'
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = 'ausi .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_words_in_parentheses_empty_string(self):
        """Test remove_words_parentheses with an empty string."""
        utterance = ''
        actual_output = SesothoCleaner.remove_words_in_parentheses(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_single(self):
        """Test remove_parentheses with 1 word partly surrounded."""
        utterance = '(ho)dula pela ausi Mamello .'
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = 'hodula pela ausi Mamello .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_multiple(self):
        """Test remove_parentheses with 3 words partly surrounded."""
        utterance = '(ho)dula pela (ho)dula (ho)dula .'
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = 'hodula pela hodula hodula .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_empty_string(self):
        """Test remove_parentheses with an empty string"""
        utterance = ''
        actual_output = SesothoCleaner.remove_parentheses(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_translation(self):
        """Test clean_translation with a timestamp."""
        translation = 'I ate it 502058_507330'
        actual_output = SesothoCleaner.clean_translation(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_with_timestamp(self):
        """Test remove_timestamp with a timestamp."""
        translation = 'I ate it 502058_507330'
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_no_timestamp(self):
        """Test remove_timestamp with no timestamp."""
        translation = 'I ate it'
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = 'I ate it'
        self.assertEqual(actual_output, desired_output)

    def test_remove_timestamp_empty_string(self):
        """Test remove_timestamp with an empty string."""
        translation = ''
        actual_output = SesothoCleaner.remove_timestamp(translation)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- cross cleaning ----------

    def test_remove_contractions_single(self):
        """Test remove contractions with one contraction."""
        seg_tier = 'e tsamay-a (u-y-e) (ho-)dul-a pela ausi Mamello .'
        gloss_tier = ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in loc '
                      'sister(1a , 2a) n^name .')
        pos_tier = ('ij v^leave-m^i (sm2s-t^p_v^go-m^s) (if-)v^sit-m^in loc '
                    'sister(1a , 2a) n^name .')
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = 'e tsamay-a (ho-)dul-a pela ausi Mamello .'
        gloss_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                          'n^name .')
        pos_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                        'n^name .')
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    def test_remove_contractions_multiple(self):
        """Test remove contractions with three contractions."""
        seg_tier = ('(u-y-e) e tsamay-a (u-y-e) (ho-)dul-a pela ausi Mamello '
                    '(u-y-e) .')
        gloss_tier = ('(sm2s-t^p_v^go-m^s) ij v^leave-m^i (sm2s-t^p_v^go-m^s) '
                      '(if-)v^sit-m^in loc sister(1a , 2a) n^name '
                      '(sm2s-t^p_v^go-m^s) .')
        pos_tier = ('(sm2s-t^p_v^go-m^s) ij v^leave-m^i (sm2s-t^p_v^go-m^s) '
                    '(if-)v^sit-m^in loc sister(1a , 2a) n^name '
                    '(sm2s-t^p_v^go-m^s) .')
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = 'e tsamay-a (ho-)dul-a pela ausi Mamello .'
        gloss_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                          'n^name .')
        pos_tier_des = ('ij v^leave-m^i (if-)v^sit-m^in loc sister(1a,2a) '
                        'n^name .')
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    def test_remove_contractions_empty_string(self):
        """Test remove contractions with an empty string."""
        seg_tier = ''
        gloss_tier = ''
        pos_tier = ''
        actual_output = SesothoCleaner.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        seg_tier_des = ''
        gloss_tier_des = ''
        pos_tier_des = ''
        desired_output = (seg_tier_des, gloss_tier_des, pos_tier_des)
        self.assertEqual(actual_output, desired_output)

    # ---------- test morpheme cleaning ----------

    def test_clean_seg_tier(self):
        """Test clean_seg tier with terminator."""
        seg_tier = 'm-ph-e ntho .'
        actual_output = SesothoCleaner.clean_seg_tier(seg_tier)
        desired_output = 'm-ph-e ntho'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier_empty_string(self):
        """Test clean_seg tier with empty string."""
        seg_tier = ''
        actual_output = SesothoCleaner.clean_seg_tier(seg_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier_standard_case(self):
        """Test clean_gloss_tier.

        Test for noun class spaces, noun class separators and
        terminators.
        """
        gloss_tier = 'n^10-bucket(9 , 10/6) ?'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier_empty_string(self):
        """Test clean_gloss_tier with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_spaces_noun_class_parentheses_standard_case(self):
        """Test remove_spaces_noun_class_parentheses."""
        gloss_tier = 'n^10-bucket(9 , 10) ?'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10)'
        self.assertEqual(actual_output, desired_output)

    def test_remove_spaces_noun_class_parentheses_empty_string(self):
        """Test remove_spaces_noun_class_parentheses with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_replace_noun_class_separator_standard_case(self):
        """Test replace_noun_class_separator with one separator."""
        gloss_tier = 'n^10-bucket(9 , 10/6)'
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_replace_noun_class_separator_empty_string(self):
        """Test replace_noun_class_separator with an empty string."""
        gloss_tier = ''
        actual_output = SesothoCleaner.clean_gloss_tier(gloss_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier_standart_case(self):
        """Test clean_pos_tier with a noun class and separator.

        Should behave the same as clean_gloss_tier.
        """
        pos_tier = 'n^10-bucket(9 , 10/6) ?'
        actual_output = SesothoCleaner.clean_pos_tier(pos_tier)
        desired_output = 'n^10-bucket(9,10|6)'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier_empty_string(self):
        """Test clean_pos_tier with an empty string.

        Should behave the same as clean_gloss_tier.
        """
        pos_tier = ''
        actual_output = SesothoCleaner.clean_pos_tier(pos_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)
    
    def test_clean_seg_word_one_pair_parentheses(self):
        """Test clean_seg_word with one pair of parentheses."""
        seg_word = '(ho)nada'
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word_two_pairs_parentheses(self):
        """Test clean_seg_word with two pairs of parentheses."""
        seg_word = '(ho)nad(a)'
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word_empty_string(self):
        """Test clean_seg_word with an empty string."""
        seg_word = ''
        actual_output = SesothoCleaner.clean_seg_word(seg_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_noun_markers_with_marker(self):
        """Test remove_noun_markers with noun_marker."""
        gloss_word = 'n^6-field(9 , 6)'
        actual_output = SesothoCleaner.remove_noun_markers(gloss_word)
        desired_output = '6-field(9 , 6)'
        self.assertEqual(actual_output, desired_output)

    def test_remove_noun_markers_empty_string(self):
        """Test remove_noun_markers with empty string."""
        gloss_word = ''
        actual_output = SesothoCleaner.remove_noun_markers(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_verb_markers_with_marker(self):
        """Test remove_verb_markers with verb_marker."""
        gloss_word = 'sm2s-t^p_v^do-m^in'
        actual_output = SesothoCleaner.remove_verb_markers(gloss_word)
        desired_output = 'sm2s-t^p_do-m^in'
        self.assertEqual(actual_output, desired_output)

    def test_remove_verb_markers_empty_string(self):
        """Test remove_verb_markers with empty string."""
        gloss_word = ''
        actual_output = SesothoCleaner.remove_verb_markers(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_name(self):
        """Test clean_proper_names_gloss_words with a name."""
        gloss_word = 'n^Name'
        actual_output = SesothoCleaner.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'a_name'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_game(self):
        """Test clean_proper_names_gloss_words with a game."""
        gloss_word = 'n^Place'
        actual_output = SesothoCleaner.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'a_place'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_no_proper_name(self):
        """Test clean_proper_names_gloss_words with not a proper name."""
        gloss_word = 'sm1s-t^p_v^be_sick-m^x'
        actual_output = SesothoCleaner.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = 'sm1s-t^p_v^be_sick-m^x'
        self.assertEqual(actual_output, desired_output)

    def test_clean_proper_names_gloss_words_empty_string(self):
        """Test clean_proper_names_gloss_words with an empty string."""
        gloss_word = ''
        actual_output = SesothoCleaner.clean_proper_names_gloss_words(
            gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_one_concatenator(self):
        """Test replace_concatenators with one concatenator."""
        gloss_word = 'sm2s-t^p_om1s-v^touch-m^in'
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = 'sm2s-t^p.om1s-v^touch-m^in'
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_multiple_concatenators(self):
        """Test replace_concatenators with three concatenators.

        But only one of them should be replaced by a dot. The others are
        verb-multi-word-expressions.

        Note: Not clear if middle '_' should be replaced.
        """
        gloss_word = 'sm2s-t^p_om1s-v^touch-m^in_v^go_out'
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = 'sm2s-t^p.om1s-v^touch-m^in_v^go_out'
        self.assertEqual(actual_output, desired_output)

    def test_replace_concatenators_empty_string(self):
        """Test replace_concatenators with an empty string."""
        gloss_word = ''
        actual_output = SesothoCleaner.replace_concatenators(gloss_word)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_nominal_concord_markers_single(self):
        """Test remove_nominal_concord_markers with 1 concord marker."""
        gloss = 'obr17'
        actual_output = SesothoCleaner.remove_nominal_concord_markers(
            gloss)
        desired_output = '17'
        self.assertEqual(actual_output, desired_output)

    def test_remove_nominal_concord_markers_empty_string(self):
        """Test remove_nominal_concord_markers with an empty string."""
        gloss = ''
        actual_output = SesothoCleaner.remove_nominal_concord_markers(
            gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_word(self):
        """Test unify_untranscibed_glosses with 'word'."""
        gloss = 'word'
        actual_output = SesothoCleaner.unify_untranscribed_glosses(gloss)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_xxx(self):
        """Test unify_untranscibed_glosses with 'xxx'."""
        gloss = 'xxx'
        actual_output = SesothoCleaner.unify_untranscribed_glosses(gloss)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscibed_glosses_empty_string(self):
        """Test unify_untranscibed_glosses with empty string."""
        gloss = ''
        actual_output = SesothoCleaner.unify_untranscribed_glosses(gloss)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_inf_standard_case(self):
        """Test remove_parentheses_inf with one pair of parentheses."""
        gloss_word = '(ho)nada'
        actual_output = SesothoCleaner.remove_parentheses(gloss_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)

    def test_remove_parentheses_inf_empty_string(self):
        """Test remove_parentheses_inf with an empty string."""
        gloss_word = '(ho)nada'
        actual_output = SesothoCleaner.remove_parentheses(gloss_word)
        desired_output = 'honada'
        self.assertEqual(actual_output, desired_output)


###############################################################################


class TestTurkishCleaner(unittest.TestCase):

    # ---------- single_morph_word ----------

    def test_single_morph_word_underscore(self):
        """Test single_morph_word with an underscore."""
        utterance = 'I have to test'
        morph_tier = 'PRON|I V|have_to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_plus(self):
        """Test single_morph_word with a plus."""
        utterance = 'I have to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_multiple_complexes(self):
        """Test single_morph_word with multiple complexes."""
        utterance = 'I have to test and I have to test'
        morph_tier = 'PRON|I V|have+to V|test CORD|and PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = 'I have_to test and I have_to test', morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_join_sep(self):
        """Test single_morph_word with no join separator."""
        utterance = 'I haveto test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_join_sep_at_end(self):
        """Test single_morph_word with no join separator at the end."""
        utterance = 'I haveto'
        morph_tier = 'PRON|I V|have+to'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex(self):
        """Test single_morph_word with no complex."""
        utterance = 'I test'
        morph_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex_misalignment1(self):
        """Test single_morph_word with no complex but with misalignment."""
        utterance = 'I test it'
        morph_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_no_complex_misalignment2(self):
        """Test single_morph_word with no complex but with misalignment."""
        utterance = 'I test'
        morph_tier = 'PRON|I V|test PRON|it'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_already_joined(self):
        """Test single_morph_word with already joined complex."""
        utterance = 'I have_to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_empty_mor(self):
        """Test single_morph_word with empty morphology tier."""
        utterance = 'I have_to test'
        morph_tier = ''
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_word_empty_utterance(self):
        """Test single_morph_word with empty utterance."""
        utterance = ''
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    def test_single_morph_unsimilar(self):
        """Test single_morph_word with unsimilar wword and mword."""
        utterance = 'I got to test'
        morph_tier = 'PRON|I V|have+to V|test'
        actual_output = TurkishCleaner.single_morph_word(utterance, morph_tier)
        desired_output = utterance, morph_tier
        self.assertEqual(actual_output, desired_output)

    # ---------- separate_morph_word ----------

    def test_separate_morph_word_underscore(self):
        """Test separate_morph_word with underscore."""
        utterance = 'bla tu_ta bla'
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta bla', 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_plus(self):
        """Test separate_morph_word with plus."""
        utterance = 'bla tu+ta bla'
        mor_tier = 'N|bla V|N|tu+V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta bla', 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_with_suffixes(self):
        """Test separate_morph_word with suffixes."""
        utterance = 'bla tuu_taa bla'
        mor_tier = 'N|bla V|N|tu-U_V|ta-A N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tuu taa bla', 'N|bla N|tu-U V|ta-A N|bla'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex(self):
        """Test separate_morph_word with no complex."""
        utterance = 'I test'
        mor_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex_misalignment1(self):
        """Test separate_morph_word with no complex but with misalignment."""
        utterance = 'I test it'
        mor_tier = 'PRON|I V|test'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_complex_misalignment2(self):
        """Test separate_morph_word with no complex but with misalignment."""
        utterance = 'I test'
        mor_tier = 'PRON|I V|test PRON|it'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_empty_mor(self):
        """Test separate_morph_word with empty morphology tier."""
        utterance = 'I have_to test'
        mor_tier = ''
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_empty_utterance(self):
        """Test separate_morph_word with empty utterance."""
        utterance = ''
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, mor_tier
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_multiple_complexes(self):
        """Test separate_morph_word with multiple complexes."""
        utterance = 'bla tu+ta tu_ta'
        mor_tier = 'N|bla V|N|tu_V|ta V|N|tu+V|ta'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = 'bla tu ta tu ta', 'N|bla N|tu V|ta N|tu V|ta'
        self.assertEqual(actual_output, desired_output)

    def test_separate_morph_word_no_join_sep(self):
        """Test separate_morph_word with no join separator."""
        utterance = 'bla tuta bla'
        mor_tier = 'N|bla V|N|tu_V|ta N|bla'
        actual_output = TurkishCleaner.separate_morph_word(utterance, mor_tier)
        desired_output = utterance, 'N|bla N|tu V|ta N|bla'
        self.assertEqual(actual_output, desired_output)

    # unify_untranscribed

    def test_unify_untranscribed_xxx_start(self):
        """Test with `xxx` at the start of utterance."""
        utterance = 'xxx great'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '??? great'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_xxx_end(self):
        """Test with `xxx` at the end of utterance."""
        utterance = 'This is xxx'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This is ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_xxx_within(self):
        """Test with `xxx` within utterance."""
        utterance = 'This xxx great'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? great'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_five_y(self):
        """Test with five `y`s."""
        utterance = 'yyyyy'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_within_word(self):
        """Test `yyy` occurring in word."""
        utterance = 'yyyia'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'yyyia'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_terminator(self):
        """Test `yyy` with terminator."""
        utterance = 'yyy.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_multiple_yyy(self):
        """Test multiple `yyy`s."""
        utterance = 'This yyy yyy good'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? ??? good'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_yyy_scoped(self):
        """Test `yyy` within scoping."""
        utterance = 'This <yyy good> [=! good]'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This <??? good> [=! good]'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_ww(self):
        """Test `ww`."""
        utterance = 'This ww good.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'This ??? good.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_x(self):
        """Test `x`."""
        utterance = 'x.'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = '???.'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_repetition(self):
        """Test repetition."""
        utterance = 'test [x 2]'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'test [x 2]'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_x_part_of_word(self):
        """Test `x` being part of a word."""
        utterance = 'Regex'
        actual_output = TurkishCleaner.unify_untranscribed(utterance)
        desired_output = 'Regex'
        self.assertEqual(actual_output, desired_output)

    # clean_utterance

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
        actual_output = TurkishCleaner.clean_utterance(utterance)
        desired_output = "that's that's ??? mine pig she said"
        self.assertEqual(actual_output, desired_output)

    # clean_word

    def test_clean_word_mixed(self):
        """Test clean_word with markers, drawls, pauses and blocking."""
        actual_output = TurkishCleaner.clean_word('^ka:+l^e@e')
        desired_output = 'ka_le'
        self.assertEqual(actual_output, desired_output)


###############################################################################


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


class TestNungonCleaner(unittest.TestCase):

    # ---------- remove_parentheses ----------

    def test_remove_parentheses(self):
        """Test remove_parentheses."""
        seg_tier = '(this is a test)'
        actual_output = NungonCleaner.remove_parentheses(seg_tier)
        desired_output = 'this is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_morph_tier ----------

    def test_clean_morph_tier(self):
        """Test clean_morph_tier."""
        morph_tier = 'PRON^this=is &=coughs ART^a N^test [laughs].'
        actual_output = NungonCleaner.clean_morph_tier(morph_tier)
        desired_output = 'PRON^this=is ART^a N^test'
        self.assertEqual(actual_output, desired_output)

    def test_clean_morph_tier_untranscribed(self):
        """Test clean_morph_tier with untranscribed morphology tier."""
        morph_tier = 'xxx'
        actual_output = NungonCleaner.clean_morph_tier(morph_tier)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- clean_seg_tier ----------

    def test_clean_seg_tier(self):
        """Test clean_seg_tier."""
        morph_tier = 'this=is &=coughs (a) test [laughs].'
        actual_output = NungonCleaner.clean_seg_tier(morph_tier)
        desired_output = 'this=is a test'
        self.assertEqual(actual_output, desired_output)

    # ---------- unify_untranscribed_morpheme_word ----------

    def test_unify_untranscribed_morpheme_word_single_question_mark(self):
        """Test unify_untranscribed_morpheme_word with single question mark."""
        word = '?'
        actual_output = NungonCleaner.unify_untranscribed_morpheme_word(word)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_untranscribed_morpheme_word_xxx(self):
        """Test unify_untranscribed_morpheme_word with xxx."""
        word = 'xxx'
        actual_output = NungonCleaner.unify_untranscribed_morpheme_word(word)
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_untranscribed_morph_tier ----------

    def test_null_untranscribed_morph_tier_single_question_mark(self):
        """Test null_untranscribed_morph_tier with single question mark."""
        utterance = '?'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_xxx(self):
        """Test null_untranscribed_morph_tier with xxx."""
        utterance = 'xxx'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_xxxx(self):
        """Test null_untranscribed_morph_tier with xxxx."""
        utterance = 'xxxx'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_with_angle_brackets(self):
        """Test null_untranscribed_morph_tier with <xxx>."""
        utterance = '<xxx>'
        actual_output = NungonCleaner.null_untranscribed_morph_tier(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_question_mark ----------

    def test_remove_question_mark(self):
        """Test remove_question_mark."""
        morpheme = '?morpheme'
        actual_output = NungonCleaner.remove_question_mark(morpheme)
        desired_output = 'morpheme'
        self.assertEqual(actual_output, desired_output)

    # ---------- remove_trailing_hashtag ----------

    def test_remove_trailing_hashtag(self):
        """Test remove_trailing_hashtag."""
        word = 'pos^gloss#'
        actual_output = NungonCleaner.remove_trailing_hashtag(word)
        desired_output = 'pos^gloss'
        self.assertEqual(actual_output, desired_output)

    # ---------- null_ambiguous_gloss_pos_word ----------

    def test_null_ambiguous_gloss_pos_word_two_variants(self):
        """Test null_ambiguous_gloss_pos_word with two variants."""
        word = 'N^mor-mor-mor#V^mor'
        actual_output = NungonCleaner.null_ambiguous_gloss_pos_word(word)
        desired_output = '???^???-???-???'
        self.assertEqual(actual_output, desired_output)

    def test_null_ambiguous_gloss_pos_word_three_variants(self):
        """Test null_ambiguous_gloss_pos_word with three variants."""
        word = 'N^mor-mor-mor#V^mor#P^mor-mor'
        actual_output = NungonCleaner.null_ambiguous_gloss_pos_word(word)
        desired_output = '???^???-???-???'
        self.assertEqual(actual_output, desired_output)

    # ---------- replace_slash ----------

    def test_replace_slash_slash_between_numbers(self):
        """Test replace_slash with slash between numbers."""
        gloss = '2/3pl'
        actual_output = NungonCleaner.replace_slash(gloss)
        desired_output = '2.3pl'
        self.assertEqual(actual_output, desired_output)

    def test_replace_slash_slash_not_between_numbers(self):
        """Test replace_slash with slash not between numbers."""
        gloss = 'test/test'
        actual_output = NungonCleaner.replace_slash(gloss)
        desired_output = 'test/test'
        self.assertEqual(actual_output, desired_output)

    # ---------- replace_slash ----------

    def test_replace_plus(self):
        """Test replace_plus."""
        gloss = '1sg+ben'
        actual_output = NungonCleaner.replace_plus(gloss)
        desired_output = '1sg.ben'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
