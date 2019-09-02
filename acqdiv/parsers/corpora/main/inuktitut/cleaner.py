import re

from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.inuktitut.gloss_mapper \
    import InuktitutGlossMapper
from acqdiv.parsers.corpora.main.inuktitut.pos_mapper \
    import InuktitutPOSMapper


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
    def clean_speaker_metadata(
            cls, session_filename, speaker_label, name, role,
            age, gender, language, birth_date, target_child):
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
                CHATUtteranceCleaner.remove_terminator,
                CHATUtteranceCleaner.null_event_utterances,
                CHATUtteranceCleaner.unify_untranscribed,
                CHATUtteranceCleaner.remove_separators,
                CHATUtteranceCleaner.remove_scoped_symbols,
                # CHATUtteranceCleaner.null_untranscribed_utterances
                ]:
            xmor = cleaning_method(xmor)

        return xmor

    # ---------- morpheme word cleaning ----------

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return CHATUtteranceCleaner.remove_terminator(morpheme_word)

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

    @classmethod
    def clean_gloss(cls, gloss):
        return InuktitutGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return InuktitutPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return InuktitutPOSMapper.map(pos_ud, ud=True)
