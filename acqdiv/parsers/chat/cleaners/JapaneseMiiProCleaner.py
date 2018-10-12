import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class JapaneseMiiProCleaner(CHATCleaner):

    @classmethod
    def remove_non_words(cls, morph_tier):
        """Remove all non-words from the morphology tier.

        Non-words have the POS tag 'tag'.
        """
        non_words_regex = re.compile(r'tag\|\S+')
        morph_tier = non_words_regex.sub('', morph_tier)
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return cls.remove_non_words(morph_tier)
