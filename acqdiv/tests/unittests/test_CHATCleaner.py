import unittest
from acqdiv.parsers.xml.CHATCleaner import CHATCleaner
from acqdiv.parsers.xml.CHATCleaner import InuktitutCleaner
from acqdiv.parsers.xml.CHATCleaner import CreeCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    Class to test the CHATCleaner.

    A lot of the test cases are taken from or inspired by
    https://talkbank.org/manuals/CHAT.pdf
    .
    """

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

    def test_handle_repetitions_empty_string(self):
        """Test handle_repetitions with an empty string."""
        actual_output = CHATCleaner.handle_repetitions('')
        desired_output = ''
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

    #TODO: test quotations

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

    # Tests for the remove_fillers-method.

    def test_remove_fillers_mutiple_fillers(self):
        """Test remove_fillers with 3 fillers (&-uh)."""
        actual_output = CHATCleaner.remove_fillers('&-uh &-uh the water &-uh')
        desired_output = 'uh uh the water uh'
        self.assertEqual(actual_output, desired_output)

    def test_remove_fillers_empty_string(self):
        """Test remove_fillers with 3 fillers (&-uh)."""
        actual_output = CHATCleaner.remove_fillers('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_pauses_within_words-method.

    def test_remove_pauses_within_words_one_pause(self):
        """Test remove_pauses with 1 pause (^)."""
        actual_output = CHATCleaner.remove_pauses_within_words('spa^ghetti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_multiple_pauses(self):
        """Test remove_pauses with 2 pauses (^)."""
        actual_output = CHATCleaner.remove_pauses_within_words(
            'spa^ghe^tti')
        desired_output = 'spaghetti'
        self.assertEqual(actual_output, desired_output)

    def test_remove_pauses_within_words_empty_string(self):
        """Test remove_pauses with an empty string."""
        actual_output = CHATCleaner.remove_pauses_within_words('')
        desired_output = ''
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

    # Test for the remove_scoped_symbols-method.

    def test_remove_scoped_symbols_not_nested(self):
        """Test remove_scoped_symbols with 2 not nested symbol pairs."""
        actual_output = CHATCleaner.remove_scoped_symbols(
            "<that's mine> [=! cries]")
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_one_level_nested(self):
        """Test remove_scoped_symbols with 1 level of nestedness."""
        actual_output = CHATCleaner.remove_scoped_symbols(
            "<that's mine [=! cries]>")
        desired_output = "that's mine"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_two_levels_nested(self):
        """Test remove_scoped_symbols with 2 levels of nestedness."""
        actual_output = CHATCleaner.remove_scoped_symbols(
            "<that's mine <she said [=! cries]>> [=! slaps leg]")
        desired_output = "that's mine she said"
        self.assertEqual(actual_output, desired_output)

    def test_remove_scoped_symbols_empty_string(self):
        """Test remove_scoped_symbols with an empty string."""
        actual_output = CHATCleaner.remove_scoped_symbols('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)


###############################################################################


class TestInuktitutCleaner(unittest.TestCase):
    """class to test the InuktitutCleaner."""

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

    # Tests for the clean_xmor-method.
    # Although the clean_xmor-method removes separators from the
    # xmor-tier such separators are not tested here, since there
    # are no occurences of separators in the xmor-tier in the
    # Inuktitut-corpus.

    def test_clean_xmor_untranscribed_and_scoped_symbols_and_terminator(self):
        """Test clean_xmor with 3 cases at once.

        Cases: untranscribed material, terminator and scoped symbols
        """
        str_input = 'xxx ! [+ UI]'
        actual_output = InuktitutCleaner.clean_xmor(str_input)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_xmor_scoped_symbol_and_terminator(self):
        """Test clean_xmor with scoped symbols and terminator."""
        str_input = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+IACT|'
                     'ai^greetings . [+ IM]')
        actual_output = InuktitutCleaner.clean_xmor(str_input)
        desired_output = ('NR|unatartusaq^soldier+NN|AUG|aluk^EMPH+'
                          'IACT|ai^greetings')
        self.assertEqual(actual_output, desired_output)

    def test_clean_xmor_empty_string(self):
        """Test clean_xmor with an empty string."""
        str_input = ''
        actual_output = InuktitutCleaner.clean_xmor(str_input)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

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
        input_str = 'NR|amaama^baby_bottle&BW NR|amaama^baby_bottle&BW'
        actual_output = InuktitutCleaner.replace_stem_gram_gloss_connector(
            input_str)
        desired_output = 'NR|amaama^baby_bottle.BW NR|amaama^baby_bottle.BW'
        self.assertEqual(actual_output, desired_output)

    def test_replace_stem_gram_gloss_connector_empty_string(self):
        """Test replace_stem_gram_gloss_connector with emtpy string."""
        actual_output = InuktitutCleaner.replace_stem_gram_gloss_connector('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_pos_separator-method.

    def test_replace_pos_separator_single_separator(self):
        """Test replace_pos_separator with 1 separator (|)."""
        input_str = 'EXCL|ai^ACT ?'
        actual_output = InuktitutCleaner.replace_pos_separator(
            input_str)
        desired_output = 'EXCL.ai^ACT ?'
        self.assertEqual(actual_output, desired_output)

    def test_replace_pos_separator_multiple_separators(self):
        """Test replace_pos_separator with 3 separators (|)."""
        input_str = 'FIL|am^um DR|u^here&SG_ST+DI|minga^MOD_SG [*] ?'
        actual_output = InuktitutCleaner.replace_pos_separator(
            input_str)
        desired_output = 'FIL.am^um DR.u^here&SG_ST+DI.minga^MOD_SG [*] ?'
        self.assertEqual(actual_output, desired_output)

    def test_replace_pos_separator_empty_string(self):
        """Test replace_pos_separator with an empty string."""
        actual_output = InuktitutCleaner.replace_pos_separator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)


###############################################################################


class TestCreeCleaner(unittest.TestCase):
    """Class to test the Cree cleaner"""

    # Tests for the remove_angle_brackets-method.

    def test_remove_angle_brackets_standard_case(self):
        """Test remove_angle_brackets with standard angle brack case."""
        input_str = '‹mâ ehtad-g› .'
        actual_output = CreeCleaner.remove_angle_brackets(input_str)
        desired_output = 'mâ ehtad-g .'
        self.assertEqual(actual_output, desired_output)

    def test_remove_angle_brackets_empty_string(self):
        """Test remove_angle_brackets with an empty string."""
        actual_output = CreeCleaner.remove_angle_brackets('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the remove_morph_separators-method.

    def test_remove_morph_separators_single_separator(self):
        """Test remove_morph_separators with 1 separator (_)."""
        input_str = 'bye_bye'
        actual_output = CreeCleaner.remove_morph_separators(input_str)
        desired_output = 'byebye'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morph_separators_multiple_separators(self):
        """Test remove_morph_separators with 2 separators (_)."""
        input_str = 'ha_ha_train'
        actual_output = CreeCleaner.remove_morph_separators(input_str)
        desired_output = 'hahatrain'
        self.assertEqual(actual_output, desired_output)

    def test_remove_morph_separators_empty_string(self):
        """Test remove_morph_separators with an empty string."""
        actual_output = CreeCleaner.remove_morph_separators('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the replace_zero-method.

    def test_replace_zero_single_zero(self):
        """Test replace_zero with 1 zero (zéro)."""
        input_str = 'puhchu~shum~zéro'
        actual_output = CreeCleaner.replace_zero(input_str)
        desired_output = 'puhchu~shum~Ø'
        self.assertEqual(actual_output, desired_output)

    def test_replace_zero_multiple_zeros(self):
        """Test replace_zero with 3 zeros (zéro)."""
        input_str = 'zéro~ʤʊ~zéro~zéro'
        actual_output = CreeCleaner.replace_zero(input_str)
        desired_output = 'Ø~ʤʊ~Ø~Ø'
        self.assertEqual(actual_output, desired_output)

    def test_replace_zero_empty_string(self):
        """Test replace_zero with an empty string."""
        actual_output = CreeCleaner.replace_zero('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_morpheme_separator-method.

    def test_replace_morpheme_separator_single_separator(self):
        """Test replace_morpheme_separator with 1 separator."""
        input_str = 'puhchu~shun'
        actual_output = CreeCleaner.replace_morpheme_separator(input_str)
        desired_output = 'puhchushun'
        self.assertEqual(actual_output, desired_output)

    def test_replace_morpheme_separator_multiple_separators(self):
        """Test replace_morpheme_separator with 2 separators."""
        input_str = 'puhchu~sum~zéro'
        actual_output = CreeCleaner.replace_morpheme_separator(input_str)
        desired_output = 'puhchusumzéro'
        self.assertEqual(actual_output, desired_output)

    def test_replace_morpheme_separator_empty_string(self):
        """Test replace_morpheme_separator with an empty string."""
        actual_output = CreeCleaner.replace_morpheme_separator('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the remove_square_brackets-method.
    # Nested brackets or multiple bracket pairs on the same line
    # are not present in the corpus and thus not tested for.

    def test_remove_square_brackets_standard_case(self):
        """Test remove_square_brackets with normal case ([...])."""
        input_str = '[ɡaɡa nɛɹa nena mətɑ]'
        actual_output = CreeCleaner.remove_square_brackets(input_str)
        desired_output = 'ɡaɡa nɛɹa nena mətɑ'
        self.assertEqual(actual_output, desired_output)

    def test_remove_square_brackets_empty_string(self):
        """Test remove_square_brackets with empty string."""
        actual_output = CreeCleaner.remove_square_brackets('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the null_untranscribed_morph_tier-method.

    def test_null_untranscribed_morph_tier_method_standard_case(self):
        """Test null_untranscribed_morph_tier with standard case (*)."""
        actual_output = CreeCleaner.null_untranscribed_morph_tier('*')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_null_untranscribed_morph_tier_method_empty_string(self):
        """Test null_untranscribed_morph_tier with empty string."""
        actual_output = CreeCleaner.null_untranscribed_morph_tier('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_eng-method.

    def test_replace_eng_single_eng(self):
        """Test replace_eng with 1 Eng to be replaced."""
        gloss_tier = 'Eng'
        utterance = 'floor'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'floor'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_multiple_engs(self):
        """Test replace_eng with 4 Engs to be replaced."""
        gloss_tier = 'remove~by. emph Eng Eng Eng Eng'
        utterance = 'min~in~ikiniu~h wâsh these are taken off'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'remove~by. emph these are taken off'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_at_beginning_end(self):
        """Test replace_eng with Engs at the start/end of the gloss."""
        gloss_tier = 'Eng fin~3.sg Eng'
        utterance = 'garbage â~u garbage'
        actual_output = CreeCleaner.replace_eng(gloss_tier, utterance)
        desired_output = 'garbage fin~3.sg garbage'
        self.assertEqual(actual_output, desired_output)

    def test_replace_eng_emtpy_string(self):
        """Test replace_eng with an empty string."""
        actual_output = CreeCleaner.replace_eng('', '')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_percentages-method.

    def test_replace_percentages_untranscribed_word(self):
        """Test replace_percentages with an untranscribed word (%%%)."""
        actual_output = CreeCleaner.replace_percentages('%%%')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_percentages_normal_word(self):
        """Test replace_percentages with a normal word."""
        actual_output = CreeCleaner.replace_percentages('hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_replace_percentages_empty_string(self):
        """Test replace_percentages with en empty string."""
        actual_output = CreeCleaner.replace_percentages('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_hashtag-method.

    def test_replace_hashtag_unglossed_word(self):
        """Test replace_hashtag with an unglossed word (%%%)."""
        actual_output = CreeCleaner.replace_hashtag('#')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_hashtag_normal_word(self):
        """Test replace_hashtag with a normal word."""
        actual_output = CreeCleaner.replace_hashtag('hey')
        desired_output = 'hey'
        self.assertEqual(actual_output, desired_output)

    def test_replace_hashtag_empty_string(self):
        """Test replace_hashtag with an empty string."""
        actual_output = CreeCleaner.replace_hashtag('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the handle_question_mark-method.

    def test_handle_question_mark_single_question_mark(self):
        """Test handle_question_mark with single question mark."""
        actual_output = CreeCleaner.handle_question_mark('?')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_handle_question_mark_question_mark_at_the_end(self):
        """Test handle_question_mark question mark at end of morph."""
        actual_output = CreeCleaner.handle_question_mark('dok?')
        desired_output = 'dok'
        self.assertEqual(actual_output, desired_output)

    def test_handle_question_mark_empty_string(self):
        """Test handle_question_mark with an empty string."""
        actual_output = CreeCleaner.handle_question_mark('dok?')
        desired_output = 'dok'
        self.assertEqual(actual_output, desired_output)

    # Tests for the replace_star-method.

    def test_replace_star_case_star(self):
        """Test handle_question_mark with a star."""
        actual_output = CreeCleaner.replace_star('*')
        desired_output = '???'
        self.assertEqual(actual_output, desired_output)

    def test_replace_star_non_star_morpheme(self):
        """Test handle_question_mark with a non star morpheme."""
        actual_output = CreeCleaner.replace_star('muw~du')
        desired_output = 'muw~du'
        self.assertEqual(actual_output, desired_output)

    def test_replace_star_empty_string(self):
        """Test handle_question_mark with an empty string."""
        actual_output = CreeCleaner.replace_star('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for replace_gloss_connector.

    def replace_gloss_connector_multiple_plus_and_comma(self):
        """Test replace_gloss_connector with 2 commas and 2 pluses."""
        gloss = 'a,quest sm+gur2 a,quest sm+gur2'
        actual_output = CreeCleaner.replace_gloss_connector(gloss)
        desired_output = 'a.quest sm.gur2 a.quest sm.gur2'
        self.assertEqual(actual_output, desired_output)

    def replace_gloss_connector_empty_string(self):
        """Test replace_gloss_connector with empty string."""
        actual_output = CreeCleaner.replace_gloss_connector('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Test for the uppercase_pos_in_parentheses-method.

    def test_uppercase_pos_in_parentheses_one_parenth_pair(self):
        """Test uppercase_pos_in_parentheses with one pair."""
        pos = 'na eˈp~o~(h)'
        actual_output = CreeCleaner.uppercase_pos_in_parentheses(pos)
        desired_output = 'na eˈp~o~(H)'
        self.assertEqual(actual_output, desired_output)

    def test_uppercase_pos_in_parentheses_empty_string(self):
        """Test uppercase_pos_in_parentheses with empty string."""
        actual_output = CreeCleaner.uppercase_pos_in_parentheses('')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
