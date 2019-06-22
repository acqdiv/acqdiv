import re

from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import BaseCHATCleaner


class EnglishManchester1Cleaner(BaseCHATCleaner):

    @classmethod
    def remove_non_words(cls, morph_tier):
        """Remove all non-words from the morphology tier.

        Non-words include:
            end|end („)
            cm|cm (,)
            bq|bq (“)
            eq|eq (”)
        """
        non_words_regex = re.compile(r'end\|end'
                                     r'|cm\|cm'
                                     r'|bq\|bq'
                                     r'|eq\|eq')

        morph_tier = non_words_regex.sub('', morph_tier)
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_terminator, cls.remove_non_words,
                cls.remove_omissions]:
            morph_tier = cleaning_method(morph_tier)

        return morph_tier

    # ---------- morpheme cleaning ----------

    # ---------- gloss cleaning ----------

    @classmethod
    def replace_ampersand(cls, gloss):
        """Replace the ampersand in glosses by a dot.

        Fusional suffixes are suffixed to the stem by an ampersand.
        Example: be&3S -> be.3S
        """
        return gloss.replace('&', '.')

    @classmethod
    def replace_zero(cls, gloss):
        """Replace ZERO in glosses by ∅."""
        return gloss.replace('ZERO', '∅')

    @classmethod
    def clean_gloss(cls, gloss):
        for cleaning_method in [cls.replace_ampersand, cls.replace_zero]:
            gloss = cleaning_method(gloss)

        return gloss

    # ---------- POS cleaning ----------

    @staticmethod
    def extract_first_pos(pos):
        """Extract the first POS tag.

        Several POS tags are separated by ':'.
        """
        return pos.split(':')[0]

    @classmethod
    def clean_pos(cls, pos):
        return cls.extract_first_pos(pos)
