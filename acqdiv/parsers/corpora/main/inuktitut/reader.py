import re

from acqdiv.parsers.chat.readers.reader import CHATReader


class InuktitutReader(CHATReader):
    """Inferences for Inuktitut."""

    def get_start_time(self):
        return self.record.dependent_tiers.get('tim', '')

    def get_end_time(self):
        return ''

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

    def get_actual_utterance(self):
        """Get the actual form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_actual_utterance()
        return self.get_actual_alternative(utterance)

    def get_target_utterance(self):
        """Get the target form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_target_utterance()
        return self.get_target_alternative(utterance)

    def get_morph_tier(self):
        return self.record.dependent_tiers.get('xmor', '')

    @staticmethod
    def iter_morphemes(word):
        """Iter POS tags, segments and glosses of a word.

        Morphemes are separated by a '+'. POS tags are on the left
        separated by a '|' from the segment. There may be several POS tags
        all separated by a '|'. The gloss is on the right separated from the
        segment by a '^'.

        Args:
            word (str): A morpheme word.

        Yields:
            tuple: The next POS tag, segment and gloss in the word.
        """
        morpheme_regex = re.compile(r'(.*)\|(.*?)\^(.*)')
        for morpheme in word.split('+'):
            match = morpheme_regex.search(morpheme)
            if match:
                yield match.group(1), match.group(2), match.group(3)
            else:
                yield '', '', ''

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for _, seg, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, _, gloss in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for pos, _, _ in cls.iter_morphemes(pos_word)]

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        if seg.endswith('@e'):
            return 'English'
        else:
            return 'Inuktitut'
