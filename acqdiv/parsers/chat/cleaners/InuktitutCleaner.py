import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class InuktitutCleaner(CHATCleaner):

    # ---------- cross cleaning ----------

    @staticmethod
    def add_birth_date(speaker_label, name, birth_date):
        if speaker_label == 'ALI' and name == 'Alec':
            birth_date = '1986-08-25'
        elif speaker_label == 'MAE' and name == 'Mae':
            birth_date = '1986-09-02'
        elif speaker_label == 'SUP' and name == 'Suusi':
            birth_date = '1986-05-17'

        return birth_date

    @classmethod
    def metadata_cross_clean(
            cls, speaker_label, name, role, age, gender, language, birth_date):
        """Add birth dates for ALI, MAE and SUP."""
        birth_date = cls.add_birth_date(speaker_label, name, birth_date)
        return speaker_label, name, role, age, gender, language, birth_date

    # ---------- word cleaning ----------

    @staticmethod
    def remove_dashes(word):
        """Remove dashes before/after xxx."""
        dash_regex = re.compile(r'-?(xxx)-?')
        return dash_regex.sub(r'\1', word)

    @classmethod
    def clean_word(cls, word):
        word = cls.remove_dashes(word)
        return super().clean_word(word)

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, xmor):
        """Clean the morphology tier 'xmor'."""
        for cleaning_method in [
                cls.remove_terminator,
                cls.null_event_utterances,
                cls.unify_untranscribed,
                cls.remove_separators,
                cls.remove_scoped_symbols,
                # cls.null_untranscribed_utterances
                ]:
            xmor = cleaning_method(xmor)

        return xmor

    # ---------- morpheme word cleaning ----------

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.remove_terminator(morpheme_word)

    # ---------- morpheme cleaning ----------

    @staticmethod
    def remove_english_marker(seg):
        """Remove the marker for english words.

        English segments are marked with the form marker '@e'.

        Args:
            seg (str): The segment.

        Returns:
            str: The segment without '@e'.
        """
        english_marker_regex = re.compile(r'(\S+)@e')
        return english_marker_regex.sub(r'\1', seg)

    @classmethod
    def clean_segment(cls, seg):
        """Remove english markers from the segment."""
        return cls.remove_english_marker(seg)

    @staticmethod
    def replace_stem_gram_gloss_connector(gloss):
        """Replace the stem and grammatical gloss connector.

        A stem gloss is connected with a grammatical gloss by an ampersand.
        The connector is replaced by a dot.

        Args:
            gloss (str): The gloss.

        Returns:
            str: The stem and grammatical connector replaced by a dot.
        """
        return gloss.replace('&', '.')

    @classmethod
    def clean_gloss(cls, gloss):
        """Replace the stem and grammatical gloss connector."""
        return cls.replace_stem_gram_gloss_connector(gloss)

    @staticmethod
    def replace_pos_separator(pos):
        """Replace the POS tag separator.

        A morpheme may have several POS tags separated by a pipe.
        POS tags to the right are subcategories of the POS tags to the left.
        The separator is replaced by a dot.

        Args:
            pos (str): The POS tag.

        Returns:
            str: POS tag separator replaced by a dot.
        """
        return pos.replace('|', '.')

    @classmethod
    def clean_pos(cls, pos):
        """Replace the POS tag separator."""
        return cls.replace_pos_separator(pos)
