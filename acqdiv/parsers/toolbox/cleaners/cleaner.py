import re

from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.timestamp import unify_timestamp


class ToolboxCleaner:

    @staticmethod
    def remove_redundant_whitespaces(string):
        """Remove redundant whitespaces."""
        string = re.sub(r'\s+', ' ', string)
        string = string.strip()
        return string

    @staticmethod
    def cross_clean(rec_dict):
        return rec_dict

    # ---------- utterance ----------

    @staticmethod
    def unify_unknown(utterance):
        return re.sub('xxx?|www|\*{3}', '???', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        """Clean up corpus-specific utterances.

        Args:
            utterance (str): The raw utterance.

        Returns:
            str: The cleaned utterance.
        """
        return cls.unify_unknown(utterance)

    @classmethod
    def clean_timestamp(cls, timestamp):
        """Clean the time stamp.

        Returns: str
        """
        return unify_timestamp(timestamp)

    # ---------- utterance word ----------

    @classmethod
    def clean_word(cls, word):
        return cls.unify_unknown(word)

    # ---------- morphology tiers ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        """No cleaning per default."""
        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(pos_tier)

    @classmethod
    def clean_lang_tier(cls, lang_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(lang_tier)

    # ---------- morpheme words ----------

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        """No cleaning per default."""
        return morpheme_word

    @classmethod
    def clean_seg_word(cls, segment_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(segment_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(pos_word)

    @classmethod
    def clean_lang_word(cls, lang_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(lang_word)

    # ---------- morphemes ----------

    @classmethod
    def clean_morpheme(cls, morpheme):
        """Clean the morpheme."""
        return ToolboxMorphemeCleaner.remove_morpheme_delimiters(morpheme)

    @classmethod
    def clean_seg(cls, segment):
        """Clean the segment."""
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss_raw(cls, gloss):
        """Clean the original gloss."""
        return cls.clean_morpheme(gloss)

    @classmethod
    def clean_gloss(cls, gloss):
        """Map original gloss to ACQDIV gloss."""
        return ''

    @classmethod
    def clean_pos_raw(cls, pos):
        """Clean the original POS tag."""
        return cls.clean_morpheme(pos)

    @classmethod
    def clean_pos(cls, pos):
        """Map original POS tag to ACQDIV POS tag."""
        return ''

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        """Map original POS tag to Universal Dependency POS tag."""
        return ''

    @classmethod
    def clean_lang(cls, lang):
        """Clean the morpheme language."""
        return cls.clean_morpheme(lang)

    @classmethod
    def clean_id(cls, id_):
        """Clean the morpheme ID."""
        return cls.clean_morpheme(id_)
