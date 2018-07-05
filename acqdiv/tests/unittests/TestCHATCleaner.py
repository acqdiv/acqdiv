import unittest
# from acqdiv.parsers.xml.CHATCleaner import CHATCleaner
from acqdiv.parsers.xml.xml_cleaner import XMLCleaner


class TestCHATCleaner(unittest.TestCase):
    """
    class to test CHATCleaner


    A lot of the test cases are taken from or inspired by
    https://
    repository.cmu.edu/cgi/viewcontent.cgi?article=1181&context=psychology
    .
    """

    def test_remove_redundant_whitespaces(self):
        """ Test the remove_redundant_whitespace-method.
        """
        self._test_leading_trailing_whitespace()
        self._test_multiple_whitespace()
        self._test_leading_trailing_tabs()
        self._test_multiple_tabs()
        self._test_leading_trailing_newlines()
        self._test_multiple_newlines()
        self._test_leading_trailing_creturns()
        self._test_multiple_creturns()
        self._test_combinations()

    def _test_leading_trailing_whitespace(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(' h '), 'h')

    def _test_multiple_whitespace(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('  h  h  '), 'h h')

    def _test_leading_trailing_tabs(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\th\t'), 'h')

    def _test_multiple_tabs(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\t\th\t\th\t\t'), 'h h')

    def _test_leading_trailing_newlines(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\nh\n'), 'h')

    def _test_multiple_newlines(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\n\nh\n\nh\n\n'), 'h h')

    def _test_leading_trailing_creturns(self):
        self.assertEqual(
            CHATCleaner.remove_redundant_whitespaces('\rh\r'), 'h')

    def _test_multiple_creturns(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\r\rh\r\rh\r\r'), 'h h')

    def _test_combinations(self):
        self.assertEqual(CHATCleaner.remove_redundant_whitespaces(
            '\n\t \r\r h   \nh \t\t\n\r'))

    def test_remove_terminator(self):
        """ Test the remove_terminator-method.

        Use all the cases described in 7.3 and 7.7 of the paper linked above.
        """
        self._test_period()
        self._test_question_mark()
        self._test_exclamation_point()
        self._test_trailing_off()
        self._test_trailing_off_of_question()
        self._test_question_with_exclamation()
        self._test_interruption()
        self._test_interruption_of_question()
        self._test_self_interruption()
        self._test_self_interrupted_question()
        self._test_transcription_break()
        self._test_CA_terminator()
        self._test_CA_begin_latch()
        self._test_quotation_on_next_line()
        self._test_quotation_precedes()

    def _test_period():
        self.assertEqual(CHATCleaner.remove_terminator(
            'I got cold.'), 'I got cold')

    def _test_question_mark():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*FAT: is that a carrot?'), '*FAT: is that a carrot')

    def _test_exclamation_point():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT: sit down!'), '*MOT: sit down')

    def _test_trailing_off():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +...'),
            '*SAR: smells good enough for ')

    def _test_trailing_off_of_question():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for +..?'),
            '*SAR: smells good enough for ')

    def _test_question_with_exclamation():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR: smells good enough for this +!?'),
            '*SAR: smells good enough for this ')

    def _test_interruption():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/.'), '*MOT:what did you ')

    def _test_interruption_of_a_question():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +/?'), '*MOT:what did you ')

    def _test_self_interruption():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for +//.'),
            '*SAR:smells good enough for ')

    def _test_self_interrupted_question():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +//?'), '*MOT:what did you ')

    def _test_transcription_break():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*SAR:smells good enough for me +.'),
            '*SAR:smells good enough for me ')

    def _test_CA_terminator():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you ++.'), '*MOT:what did you ')

    def _test_CA_begin_latch():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*MOT:what did you +=.'), '*MOT:what did you ')

    def _test_quotation_on_next_line():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*CHI:and then the little bear said +”/.'),
            '*CHI:and then the little bear said ')

    def _test_quotation_precedes():
        self.assertEqual(CHATCleaner.remove_terminator(
            '*CHI:+” please give me all of your honey.'),
            '*CHI: please give me all of your honey.')

    def test_null_untranscribed_utterances():
        """ Test the null_untranscribed-mehtod.
        """

        self._test_xxx()
        self._test_normal_utt()

    def _test_xxx():
        self.assertEqual(CHATCleaner.null_untranscribed_utterances('xxx'), '')

    def _test_normal_utt():
        self.assertEqual(CHATCleaner.null_untranscribed_utterances(
            'Hey there'), 'Hey there')

    def test_null_event_utterances():
        """ Test the null_event_utterances-method.
        """
        self._test_null()
        self._test_normal_utt()
        # is it ok to reuse the _test_normal_utt-method?

    def _test_null():
        self.assertEqual(CHATCleaner.null_untranscribed_utterances('0'), '')

    def test_remove_events():
        """ Test the remove_events-method.
        """
        self._test_single_event()
        self._test_multiple_events()

    def _test_single_event():
        self.assertEqual(CHATCleaner.remove_events(
            'Hey there &=coughs'), 'Hey there ')

    def _test_multiple_events():
        self.assertEqual(CHATCleaner.remove_events(
            '&=gasps I got &=groans cold. &=vocalizes'), ' I got cold. ')

    def test_handle_repetitions():
        """ Test the handle_repetitions-method.
        """
        self._test_single_repetition()
        self._test_multiple_repetitions()
        # should I test for bad notation like negative numbers?

    def _test_single_repetition():
        self.assertEqual(CHATCleaner.handle_repetitions(
            "it's [x 4] like a um dog."), "it's it's it's it's like a um dog.")

    def _test_multiple_repetitions():
        self.assertEqual(CHATCleaner.handle_repetitions(
            'Hey [x 2] there [x 3]'), 'Hey hey there there there')
        # desired to write second 'hey' not with capital-h?

    def test_remove_omissions():
        """ Test the remove_omissions-method.
        """
        self._test_single_omission()
        self._test_multiple_omissions()
        self._test_omission_with_marker()  # test for omission with marker?

    def _test_single_omission():
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is my truck?'), 'where my truck?')

    def _test_multiple_omissions():
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is 0my truck?'), 'where truck?')

    def _test_omission_with_marker():
        self.assertEqual(CHATCleaner.remove_omissions(
            'where 0is [*] my truck?'), 'where my truck?')

    def test_unify_untranscribed():
        """ Test the unify_untranscribed-method.
        """
        self._test_untranscribed_xyz()

    def _test_untranscribed_xyz():
        self.assertEqual(CHATCleaner.remove_omissions(
            'zzz xxx yyy truck?'), 'xxx xxx xxx truck?')

    def test_remove_form_markers():
        """ Test the remove-form-markers-method.
        """
        self._test_l_marked()
        self._test_k_marked()

    def _test_l_marked():
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's m@l a@l r@l k@l."), "it's m a r k.")

    def _test_k_marked():
        self.assertEqual(CHATCleaner.remove_form_markers(
            "it's mark@k."), "it's mark")

    def test_remove_linkers():
        """ Test the remove_linkers-method.
        """
        # TODO


if __name__ == '__main__':
    unittest.main()
