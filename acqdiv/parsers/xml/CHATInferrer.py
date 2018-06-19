import re


class CHATInferrer:
    """Infer data from parts of CHAT record.

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


class InuktitutInferrer(CHATInferrer):
    """Inferences for Inuktitut."""

    @staticmethod
    def get_actual_alternative(utterance):
        """Get the actual form of alternatives.

        Coding in CHAT: [=? <words>]
        The actual form is the alternative given in brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[=\? (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_target_alternative(utterance):
        """Get the target form of alternatives.

        Coding in CHAT: [=? <words>]
        The target form is the original form.
        """
        # several scoped words
        alternative_regex1 = re.compile(r'<(.*?)> \[=\? .*?\]')
        clean = alternative_regex1.sub(r'\1', utterance)
        # one scoped word
        alternative_regex2 = re.compile(r'(\S+) \[=\? .*?\]')
        return alternative_regex2.sub(r'\1', clean)

    @staticmethod
    def get_segments(xmor):
        """Get segments from the xmor tier."""
        pass

    @staticmethod
    def get_pos(xmor):
        """Get the POS tags from the xmor tier.

        Coding: POS tags are prefixed to the segment via |. If the segment has
        several POS tags, the tags to the right are more specific. Such
        subcategories of POS tags are added by | and replaced by a dot.

        Returns:
            list: list of POS tags.
        """
        pos_regex = re.compile(r'(\w+\|)+')
        pos_list = []
        # go through all POS tags
        for pos_match in pos_regex.finditer(xmor):
            pos = pos_match.group()
            # strip | at the end
            pos = pos.rstrip('|')
            # replace | by . in case of subcategories
            pos = pos.replace('|', '.')
            pos_list.append(pos)

        return pos_list

    @staticmethod
    def get_glosses(xmor):
        """Get the glosses from the xmor tier."""
        pass


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

    inuktitut_inferrer = InuktitutInferrer()
    print(repr(inuktitut_inferrer.get_actual_alternative(
        'This is the target [=? actual] form.')))
    print(repr(inuktitut_inferrer.get_target_alternative(
        'This is the target [=? actual] form.')))

    test = 'LR|qa^outside+LI|unnga^ALL+VZ|aq^go_by_way_of+VV|VA|' \
           'tit^CAUS+VV|lauq^POL+VI|nnga^IMP_2sS_1sO'

    print(repr(inuktitut_inferrer.get_pos(test)))
