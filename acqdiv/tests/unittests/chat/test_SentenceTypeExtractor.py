import unittest
from acqdiv.parsers.chat.readers.SentenceTypeExtractor \
    import SentenceTypeExtractor as SentTypExtr


class SentenceTypeExtractor(unittest.TestCase):

    # ---------- get_utterance_terminator ----------

    def test_get_utterance_terminator_space_before(self):
        """Test get_utterance_terminator with space before."""
        utterance = 'Das ist ein Test .'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_space_before(self):
        """Test get_utterance_terminator with no space before."""
        utterance = 'Das ist ein Test.'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode(self):
        """Test get_utterance_terminator with postcode."""
        utterance = 'Das ist ein Test . [+ postcode]'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_no_space(self):
        """Test get_utterance_terminator with postcode and no space."""
        utterance = 'Das ist ein Test .[+ postcode]'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_multiple_spaces(self):
        """Test get_utterance_terminator with postcode and multiple spaces."""
        utterance = 'Das ist ein Test .  [+ postcode]'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_non_terminator_dot(self):
        """Test get_utterance_terminator with a non-terminator dot."""
        utterance = 'Das ist (.) ein Test ? [+ postcode]'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_terminator(self):
        """Test get_utterance_terminator with no terminator."""
        utterance = 'Das ist ein Test'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_empty_string(self):
        """Test get_utterance_terminator with empty string."""
        utterance = ''
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question(self):
        """Test get_utterance_terminator with question mark."""
        utterance = 'this is a test ?'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_exclamation(self):
        """Test get_utterance_terminator with exclamation mark."""
        utterance = 'this is a test !'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '!'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_broken_for_coding(self):
        """Test get_utterance_terminator with broken-for-coding mark."""
        utterance = 'this is a test +.'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off(self):
        """Test get_utterance_terminator with trail-off mark."""
        utterance = 'this is a test +...'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+...'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off_of_a_question(self):
        """Test get_utterance_terminator with trail-off-of-a-question mark."""
        utterance = 'this is a test +..?'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+..?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question_with_exclamation(self):
        """Test get_utterance_terminator with question-exclamation mark."""
        utterance = 'this is a test +!?'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+!?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption(self):
        """Test get_utterance_terminator with interruption mark."""
        utterance = 'this is a test +/.'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption_of_a_question(self):
        """Test get_utterance_terminator with interruption-question mark."""
        utterance = 'this is a test +/?'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+/?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interruption(self):
        """Test get_utterance_terminator with self-interruption mark."""
        utterance = 'this is a test +//.'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+//.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interrupted_question(self):
        """Test get_utterance_terminator with self-interrupted-question."""
        utterance = 'this is a test +//?'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+//?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_follows(self):
        """Test get_utterance_terminator with quotation-follows mark."""
        utterance = 'this is a test +"/.'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+"/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_precedes(self):
        """Test get_utterance_terminator with quotation-precedes mark."""
        utterance = 'this is a test +".'
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '+".'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trailing_whitespace(self):
        """Test get_utterance_terminator with trailing whitespace."""
        utterance = 'Is this a test ? '
        actual_output = SentTypExtr.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)