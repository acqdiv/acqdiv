import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.CHATUtteranceCleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.english.EnglishGlossMapper \
    import EnglishGlossMapper
from acqdiv.parsers.corpora.main.english.EnglishPOSMapper \
    import EnglishPOSMapper


class EnglishManchester1Cleaner(CHATCleaner):

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
        return CHATUtteranceCleaner.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                CHATUtteranceCleaner.remove_terminator, cls.remove_non_words,
                CHATUtteranceCleaner.remove_omissions]:
            morph_tier = cleaning_method(morph_tier)

        return morph_tier

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return EnglishGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return EnglishPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return EnglishPOSMapper.map(pos_ud, ud=True)
