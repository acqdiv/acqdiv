import re


class SentenceTypeExtractor:
    """Methods for inferring the sentence type of a CHAT utterance."""

    @classmethod
    def get_sentence_type(cls, utterance):
        """Get the sentence type of the utterance.

        Args:
            utterance (str): The utterance.

        Returns:
            str: The sentence type.
        """
        terminator = cls.get_utterance_terminator(utterance)
        sentence_type = cls.terminator2sentence_type(terminator)
        return sentence_type

    @staticmethod
    def get_utterance_terminator(utterance):
        terminator_regex = re.compile(r'([+/.!?"]*[!?.])(?=(\s*\[\+|\s*$))')
        match = terminator_regex.search(utterance)
        if match:
            return match.group(1)
        else:
            return ''

    @staticmethod
    def terminator2sentence_type(terminator):
        """Map utterance terminator to sentence type.

        Returns:
            str: The sentence type.
        """
        mapping = {'.': 'default',
                   '?': 'question',
                   '!': 'exclamation',
                   '+.': 'transcription break',
                   '+...': 'trail off',
                   '+..?': 'trail off of question',
                   '+!?': 'question with exclamation',
                   '+/.': 'interruption',
                   '+/?': 'interruption of a question',
                   '+//.': 'self-interruption',
                   '+//?': 'self-interrupted question',
                   '+"/.': 'quotation follows',
                   '+".': 'quotation precedes'}

        return mapping.get(terminator, '')
