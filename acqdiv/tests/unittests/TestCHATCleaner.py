import unittest
from acqdiv.parsers.xml.CHATCleaner import CHATCleaner
# from acqdiv.parsers.xml.xml_cleaner import XMLCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    class to test CHATCleaner


    A lot of the test cases are taken from or inspired by
    https://
    repository.cmu.edu/cgi/viewcontent.cgi?article=1181&context=psychology
    .
    """

    # def test_remove_redundant_whitespaces(self):
    #     """ Test the remove_redundant_whitespace-method.
    #     """
    #     self._test_leading_trailing_whitespace()
    #     self._test_multiple_whitespace()
    #     self._test_leading_trailing_tabs()
    #     self._test_multiple_tabs()
    #     self._test_leading_trailing_newlines()
    #     self._test_multiple_newlines()
    #     self._test_leading_trailing_creturns()
    #     self._test_multiple_creturns()
    #     self._test_combinations()

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

    # def test_remove_terminator(self):
    #     """ Test the remove_terminator-method.

    #     Use all the cases described in 7.3 and 7.7 of the paper linked above.
    #     """
    #     self._test_period()
    #     self._test_question_mark()
    #     self._test_exclamation_point()
    #     self._test_trailing_off()
    #     self._test_trailing_off_of_question()
    #     self._test_question_with_exclamation()
    #     self._test_interruption()
    #     self._test_interruption_of_question()
    #     self._test_self_interruption()
    #     self._test_self_interrupted_question()
    #     self._test_transcription_break()
    #     self._test_CA_terminator()
    #     self._test_CA_begin_latch()
    #     self._test_quotation_on_next_line()
    #     self._test_quotation_precedes()

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
            '*SAR: smells good enough for ')

    def test_trailing_off_of_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +..?'),
            '*SAR: smells good enough for ')

    def test_question_with_exclamation(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?'),
            '*SAR: smells good enough for this ')

    def test_interruption(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/.'), '*MOT:what did you ')

    def test_interruption_of_a_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/?'), '*MOT:what did you ')

    def test_self_interruption(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for +//.'),
            '*SAR:smells good enough for ')

    def test_self_interrupted_question(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +//?'), '*MOT:what did you ')

    def test_transcription_break(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for me +.'),
            '*SAR:smells good enough for me ')

    def test_CA_terminator(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you ++.'), '*MOT:what did you ')

    def test_CA_begin_latch(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +=.'), '*MOT:what did you ')

    def test_quotation_on_next_line(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*CHI:and then the little bear said +”/.'),
            '*CHI:and then the little bear said ')

    def test_quotation_precedes(self):
        self.assertEqual(CHATCleaner.remove_terminator(
            '*CHI:+” please give me all of your honey.'),
            '*CHI: please give me all of your honey.')

    # def test_null_untranscribed_utterances(self):
    #     """ Test the null_untranscribed-mehtod.
    #     """

    #     self._test_xxx()
    #     self._test_normal_utt()

    def test_xxx(self):
        self.assertEqual(CHATCleaner.null_untranscribed_utterances('xxx'), '')

    def test_normal_utt(self):
        self.assertEqual(CHATCleaner.null_untranscribed_utterances(
            'Hey there'), 'Hey there')

    # def test_null_event_utterances(self):
    #     """ Test the null_event_utterances-method.
    #     """
    #     self._test_null()
    #     self._test_normal_utt()
    #     # is it ok to reuse the _test_normal_utt-method?

    def test_null(self):
        self.assertEqual(CHATCleaner.null_event_utterances('0'), '')

    # def test_remove_events(self):
    #     """ Test the remove_events-method.
    #     """
    #     self._test_single_event()
    #     self._test_multiple_events()

    def test_single_event(self):
        self.assertEqual(CHATCleaner.remove_events(
            'Hey there &=coughs'), 'Hey there ')

    def test_multiple_events(self):
        self.assertEqual(CHATCleaner.remove_events(
            '&=gasps I got &=groans cold. &=vocalizes'), ' I got cold. ')

    # def test_handle_repetitions(self):
    #     """ Test the handle_repetitions-method.
    #     """
    #     self._test_single_repetition()
    #     self._test_multiple_repetitions()
    #     # should I test for bad notation like negative numbers?

    def test_single_repetition(self):
        self.assertEqual(CHATCleaner.handle_repetitions(
            "it's [x 4] like a um dog."), "it's it's it's it's like a um dog.")

    def test_multiple_repetitions(self):
        self.assertEqual(CHATCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]'), 'Hey hey there there there')
        # desired to write second 'hey' not with capital-h?

    # def test_remove_omissions(self):
    #     """ Test the remove_omissions-method.
    #     """
    #     self._test_single_omission()
    #     self._test_multiple_omissions()
    #     self._test_omission_with_marker()  # test for omission with marker?

    def test_single_omission(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is my truck?'), 'where my truck?')

    def test_multiple_omissions(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is 0my truck?'), 'where truck?')

    def test_omission_with_marker(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is [*] my truck?'), 'where my truck?')

    # def test_unify_untranscribed(self):
    #     """ Test the unify_untranscribed-method.
    #     """
    #     self._test_untranscribed_xyz()

    def test_untranscribed_xyz(self):
        self.assertEqual(CHATCleaner.remove_omissions(
            'zzz xxx yyy truck?'), 'xxx xxx xxx truck?')

    # def test_remove_form_markers(self):
    #     """ Test the remove-form-markers-method.
    #     """
    #     self._test_l_marked()
    #     self._test_k_marked()

    def test_l_marked(self):
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's m@l a@l r@l k@l."), "it's m a r k.")

    def test_k_marked(self):
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's mark@k."), "it's mark")

    # def test_remove_linkers(self):
    #     """ Test the remove_linkers-method.
    #     """
    #     # TODO


if __name__ == '__main__':
    unittest.main()
