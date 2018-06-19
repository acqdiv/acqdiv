import re

class CHATInferrer:
    """Infer information from CHAT tiers.

    Provides the following generic inferences:
        - actual form of utterance
        - target form of utterance
        - sentence type of utterance
    """

    @staticmethod
    def get_shortening_actual(utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: parentheses within word.
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(\S*)\(\S+\)(\S*)')
        return shortening_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_shortening_target(utterance):
        """Get the target form of shortenings.

        Coding in CHAT: \w+(\w+)\w+ .
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(\S*)\((\S+)\)(\S*)')
        return shortening_regex.sub(r'\1\2\3', utterance)

    @staticmethod
    def get_replacement_actual(utterance):
        """Get the actual form of replacements.

        Coding in CHAT: [: <words>] .
        Keeps replaced words, removes replacing words with brackets.
        """
        # several scoped words
        replacement_regex1 = re.compile(r'<(.*?)> \[: .*?\]')
        clean = replacement_regex1.sub(r'\1', utterance)
        # one scoped word
        replacement_regex2 = re.compile(r'(\S+) \[: .*?\]')
        return replacement_regex2.sub(r'\1', clean)

    @staticmethod
    def get_replacement_target(utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words with brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[: (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_actual(utterance):
        """Get the actual form of fragments.

        Coding in CHAT: word starting with &.
        Keeps the fragment, removes the & from the word.
        """
        fragment_regex = re.compile(r'&(\S+)')
        return fragment_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'&\S+')
        return fragment_regex.sub('xxx', utterance)

    @classmethod
    def get_actual_form(cls, utterance):
        """Get the actual form of the utterance."""
        for actual_method in [cls.get_shortening_actual,
                              cls.get_fragment_actual,
                              cls.get_replacement_actual]:
            utterance = actual_method(utterance)

        return utterance

    @classmethod
    def get_target_form(cls, utterance):
        """Get the target form of the utterance."""
        for target_method in [cls.get_shortening_target,
                              cls.get_fragment_target,
                              cls.get_replacement_target]:
            utterance = target_method(utterance)

        return utterance

    @staticmethod
    def get_sentence_type(utterance):
        """Get the sentence type of an utterance.

        The sentence type is inferred from the utterance terminator.
        """
        mapping = {'.': 'declarative',
                   '?': 'question',
                   '!': 'exclamation',
                   '+.': 'broken for coding',
                   '+..': 'trail off',
                   '+..?': 'trail off of question',
                   '+!?': 'question with exclamation',
                   '+/.': 'interruption',
                   '+/?': 'interruption of a question',
                   '+//.': 'self-interruption',
                   '+//?': 'self-interrupted question',
                   '+"/.': 'quotation follows',
                   '+".': 'quotation precedes'}
        terminator_regex = re.compile(r'([+/.!?"]*[!?.])(?=( \[\+|$))')
        match = terminator_regex.search(utterance)
        return mapping[match.group(1)]


if __name__ == '__main__':
    inferrer = CHATInferrer()
    print(repr(inferrer.get_shortening_actual(
        'This (i)s a short(e)ned senten(ce)')))
    print(repr(inferrer.get_shortening_target(
        'This (i)s a short(e)ned senten(ce)')))
    print(repr(inferrer.get_replacement_actual(
        'This us [: is] <srane suff> [: strange stuff]')))
    print(repr(inferrer.get_replacement_target(
        'This us [: is] <srane suff> [: strange stuff]')))
    print(repr(inferrer.get_fragment_actual('This is &at .')))
    print(repr(inferrer.get_fragment_target('This is &at .')))
    print(repr(inferrer.get_sentence_type('This is a sent +!?')))