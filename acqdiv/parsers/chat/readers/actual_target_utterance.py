import re


class ActualTargetUtteranceExtractor:
    """Methods for extracting actual and target utterances."""

    @classmethod
    def to_actual_utterance(cls, utterance):
        """Extract actual utterance."""
        for actual_method in [cls.get_shortening_actual,
                              cls.get_fragment_actual,
                              cls.get_replacement_actual]:
            utterance = actual_method(utterance)

        return utterance

    @classmethod
    def to_target_utterance(cls, utterance):
        """Extract target utterance."""
        for target_method in [cls.get_shortening_target,
                              cls.get_fragment_target,
                              cls.get_replacement_target]:
            utterance = target_method(utterance)

        return utterance

    @staticmethod
    def get_shortening_actual(utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: parentheses within word.
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(?<=\S)\(\S+?\)|\(\S+?\)(?=\S)')
        return shortening_regex.sub('', utterance)

    @staticmethod
    def get_shortening_target(utterance):
        """Get the target form of shortenings.

        Coding in CHAT: parentheses within word.
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(?<=\S)\((\S+?)\)|\((\S+?)\)(?=\S)')
        return shortening_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_replacement_actual(utterance):
        """Get the actual form of replacements.

        Coding in CHAT: [: <words>] .
        Keeps replaced words, removes replacing words with brackets.
        """
        # several scoped words
        replacement_regex1 = re.compile(r'<(.*?)> ?\[: .*?\]')
        clean = replacement_regex1.sub(r'\1', utterance)
        # one scoped word
        replacement_regex2 = re.compile(r'(\S+) ?\[: .*?\]')
        return replacement_regex2.sub(r'\1', clean)

    @staticmethod
    def get_replacement_target(utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words within brackets. If there
        is more than one replacing word, they are joined together by an
        underscore.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) ?\[: (.*?)\]')

        def x(match):
            return match.group(1).replace(' ', '_')

        return replacement_regex.sub(x, utterance)

    @staticmethod
    def get_fragment_actual(utterance):
        """Get the actual form of fragments.

        Coding in CHAT: word starting with &.
        Keeps the fragment, removes the & from the word.
        """
        fragment_regex = re.compile(r'(^|\s)&([^-=\s]\S*)')
        return fragment_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'(^|\s)&([^-=\s]\S*)')
        return fragment_regex.sub(r'\1xxx', utterance)

    @staticmethod
    def get_retracing_actual(utterance):
        """Get the actual form of retracings.

        Coding in CHAT: [/], [//], [///], [/-]

        Removal of retracing markers.
        """
        # several scoped words
        retracing_regex1 = re.compile(r'<(.*?)> ?\[(/{1,3}|/-)\]')
        clean = retracing_regex1.sub(r'\1', utterance)
        # one scoped word
        retracing_regex2 = re.compile(r'(\S+) ?\[(/{1,3}|/-)\]')
        return retracing_regex2.sub(r'\1', clean)

    @classmethod
    def get_retracing_target(cls, utterance):
        """Get the target form of retracings.

        Coding in CHAT: [/], [//], [///], [/-]

        Same treatment as the actual form, except for single-word
        corrections in which both the retraced and retracing part receive
        the retracing value, e.g. hui [//] hoi du -> hoi hoi du. Multiple words
        being corrected cannot be replaced by their target forms since the
        correcting part can be of variable length.
        """
        # single-word correction
        retracing_regex = re.compile(r'([^>\s]+) ?\[//\] (\S+)')
        utterance = retracing_regex.sub(r'\2 \2', utterance)
        return cls.get_retracing_actual(utterance)
