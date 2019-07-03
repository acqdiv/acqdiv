import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import \
    CHATCleaner

from acqdiv.parsers.chat.cleaners.CHATUtteranceCleaner \
    import CHATUtteranceCleaner

from acqdiv.parsers.chat.cleaners.CHATWordCleaner import CHATWordCleaner


class BaseCHATCleaner(CHATCleaner):
    """Clean parts of a CHAT record.

    This class provides a range of cleaning methods that perform modifications,
    additions or removals to parts of a CHAT record. Redundant whitespaces that
    are left by a cleaning operation are always removed, too.

    The order of calling the cleaning methods has great impact on the final
    result, e.g. handling of repetitions has to be done first, before
    scoped symbols are removed.

    If the docstring of a cleaning method does not explicitly contain argument
    or return information, the method will only accept strings as arguments
    and return a cleaned version of the string.
    """
    # ---------- metadata cleaning ----------

    @staticmethod
    def clean_date(date):
        """Clean the date.

        CHAT date format:
            day-month-year
            \d\d-\w\w\w-\d\d\d\d
        """
        mapping = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
                   'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                   'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
        if not date:
            return ''
        else:
            day, month, year = date.split('-')
            month_clean = mapping[month]
            return '-'.join([year, month_clean, day])

    # ---------- utterance cleaning ----------

    @staticmethod
    def clean_record_speaker_label(session_filename, speaker_label):
        """No cleaning by default."""
        return speaker_label

    @classmethod
    def clean_utterance(cls, utterance):
        return CHATUtteranceCleaner.clean(utterance)

    @staticmethod
    def clean_translation(translation):
        """No cleaning by default."""
        return translation

    # ---------- word cleaning ----------

    @classmethod
    def clean_word(cls, word):
        return CHATWordCleaner.clean(word)

    # ---------- morphology tier cleaning ----------
    @staticmethod
    def clean_morph_tier(morph_tier):
        """No cleaning by default."""
        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.clean_morph_tier(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.clean_morph_tier(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.clean_morph_tier(pos_tier)

    # ---------- cross cleaning ----------

    @staticmethod
    def clean_session_metadata(session_filename, date, media_filename):
        """No cleaning by default."""
        return date, media_filename

    @staticmethod
    def clean_speaker_metadata(
            session_filename, speaker_label, name, role, age,
            gender, language, birth_date, target_child):
        """No cleaning by default."""
        return speaker_label, name, role, age, gender, language, birth_date

    @staticmethod
    def utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier):
        """No cleaning by default."""
        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

    # ---------- morpheme word cleaning ----------
    @staticmethod
    def clean_morpheme_word(morpheme_word):
        """No cleaning by default."""
        return morpheme_word

    @classmethod
    def clean_seg_word(cls, seg_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(seg_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(pos_word)

    # ---------- morpheme cleaning ----------

    @staticmethod
    def clean_morpheme(morpheme):
        """No cleaning by default."""
        return morpheme

    @classmethod
    def clean_segment(cls, segment):
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss(cls, gloss):
        return cls.clean_morpheme(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return cls.clean_morpheme(pos)
