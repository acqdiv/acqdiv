import re

from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.nungon.gloss_mapper \
    import NungonGlossMapper
from acqdiv.parsers.corpora.main.nungon.pos_mapper \
    import NungonPOSMapper


class NungonCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @staticmethod
    def null_untranscribed_morph_tier(morph_tier):
        """Null utterances containing only untranscribed material.

        Untranscribed morphology tiers are either '?' or 'xxx{3,}' or <xxx>.

        Note:
            Nulling means here the utterance is returned as an empty string.
        """
        if re.fullmatch(r'\?|<?x{3,}>?', morph_tier):
            return ''
        else:
            return morph_tier

    @staticmethod
    def remove_parentheses(seg_tier):
        """Remove parentheses in the segment tier.

        Only one case.
        """
        return seg_tier.replace('(', '').replace(')', '')

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                CHATUtteranceCleaner.remove_scoped_symbols,
                CHATUtteranceCleaner.remove_events,
                CHATUtteranceCleaner.remove_terminator,
                cls.null_untranscribed_morph_tier]:
            morph_tier = cleaning_method(morph_tier)

        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        seg_tier = cls.remove_parentheses(seg_tier)
        return cls.clean_morph_tier(seg_tier)

    # ---------- morpheme word cleaning ----------

    @staticmethod
    def unify_untranscribed_morpheme_word(morpheme_word):
        """Unify untranscribed morpheme words.

        Untranscribed morpheme words are either '?' or xxx{3,}.
        """
        if re.fullmatch(r'\?|x{3,}', morpheme_word):
            return '???'
        else:
            return morpheme_word

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.unify_untranscribed_morpheme_word(morpheme_word)

    @staticmethod
    def remove_trailing_hashtag(gloss_pos_word):
        """Remove a trailing # from the gloss/POS word."""
        return gloss_pos_word.rstrip('#')

    @staticmethod
    def null_ambiguous_gloss_pos_word(gloss_pos_word):
        """Null ambiguous gloss/POS word.

        Ambiguous segment words are coded on the gloss/POS word. Variants are
        separated by #. The structure of the first variant is taken and every
        morpheme in it is set to ???.
        """
        if '#' in gloss_pos_word:
            variants = gloss_pos_word.split('#')
            variant = variants[0]
            return re.sub(r'[^-^]+', '???', variant)
        else:
            return gloss_pos_word

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        gloss_word = cls.remove_trailing_hashtag(gloss_word)
        gloss_word = cls.null_ambiguous_gloss_pos_word(gloss_word)
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        pos_word = cls.remove_trailing_hashtag(pos_word)
        pos_word = cls.null_ambiguous_gloss_pos_word(pos_word)
        return cls.clean_morpheme_word(pos_word)

    # ---------- morpheme cleaning ----------

    @staticmethod
    def remove_question_mark(morpheme):
        """Remove the question mark in the morpheme.

        Question marks might code insecure annotations. They are prefixed to
        the morpheme.
        """
        return morpheme.lstrip('?')

    @classmethod
    def clean_segment(cls, segment):
        return cls.remove_question_mark(segment)

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return NungonGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return NungonPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return NungonPOSMapper.map(pos_ud, ud=True)
