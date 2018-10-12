import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class YucatecCleaner(CHATCleaner):

    # ---------- utterance cleaning ----------

    # TODO: removing dashes in utterance?

    @classmethod
    def remove_terminator(cls, utterance):
        """Remove utterance terminator.

        Also removes the colon and the dash.
        """
        utterance = super().remove_terminator(utterance)
        return utterance.rstrip('-').rstrip(':')

    # ---------- morphology tier cleaning ----------

    @classmethod
    def remove_double_hashes(cls, morph_tier):
        """Remove ## from the morphology tier."""
        morph_tier = re.sub(r'(^| )##( |$)', r'\1\2', morph_tier)
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_terminator, cls.remove_double_hashes]:
            morph_tier = cleaning_method(morph_tier)

        return morph_tier

    # ---------- morpheme word cleaning ----------

    @staticmethod
    def correct_hyphens(morpheme_word):
        """Replace faulty hyphens by the pipe in the morpheme word.

        It is only attested in suffixes, not in prefixes.
        """
        return re.sub(r'(:[A-Z0-9]+)-(?=[a-záéíóúʔ]+)', r'\1|', morpheme_word)

    @staticmethod
    def remove_colon(morpheme_word):
        """Remove leading and trailing colons.

        Note:
            In some cases, the colons are correct, but a whitespace to the
            preceding or following morpheme was erroneously inserted. This
            case is not handled as the inference rules would be quite complex.
        """
        return morpheme_word.strip(':')

    @staticmethod
    def remove_dash(word_morpheme):
        """Remove leading and trailing dash.

        Note:
            In some cases, the dashes are correct, but a whitespace to the
            preceding or following morpheme was erroneously inserted. This
            case is not handled as the inference rules would be quite complex.
        """
        return word_morpheme.strip('-')

    @staticmethod
    def remove_colon_dash(word_morpheme):
        """Remove trailing colon and dash.

        Note:
            In some cases, they are correct, but a whitespace to the
            preceding or following morpheme was erroneously inserted. This
            case is not handled as the inference rules would be quite complex.
        """
        return word_morpheme.rstrip('-').rstrip(':')

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        for cleaning_method in [
                cls.correct_hyphens, cls.remove_colon, cls.remove_dash,
                cls.remove_colon_dash]:
            morpheme_word = cleaning_method(morpheme_word)
        return morpheme_word

    # ---------- morpheme cleaning ----------

    @staticmethod
    def replace_colon(morpheme):
        """Replace the colon by a dot.

        Args:
            morpheme (str): gloss or POS tag
        """
        return morpheme.replace(':', '.')

    @classmethod
    def clean_gloss(cls, gloss):
        return cls.replace_colon(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return cls.replace_colon(pos)
