from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner

from acqdiv.parsers.chat.cleaners.word_cleaner import CHATWordCleaner
from acqdiv.util.timestamp import unify_timestamp


class CHATCleaner:
    """Default cleaner for CHAT corpora."""

    @staticmethod
    def clean_date(date):
        """Clean the date.

        Prescribed format:
            year-month-day
            YYYY-MM-DD

        Returns: str
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

    @staticmethod
    def clean_age(age):
        """Reformat age in CHAT corpora.

        CHAT ages are usually given in the format YY;MM.DD. If month and day is
        missing, it is given in the format 'YY;'. If only the day is missing, it is
        given in the format 'YY;MM.'. Missing values will be converted to 0:
        'YY;0.0' or 'YY:MM.0'.

        Args:
            age (str): The raw age.

        Returns:
            str: The reformatted age.
        """
        if age:
            # month and day is missing
            if age.endswith(';'):
                age += '0.0'
            # day is missing
            elif age.endswith('.'):
                age += '0'

        return age

    @staticmethod
    def clean_gender(gender):
        """Clean the gender.

        Returns: str
        """
        return gender.title()

    @staticmethod
    def clean_name(name):
        """Clean the name.

        Returns: str
        """
        return name

    @staticmethod
    def clean_record_speaker_label(session_filename, speaker_label):
        """Clean the speaker label in a record.

        No cleaning by default.

        Returns:
            str: The cleaned speaker label.
        """
        return speaker_label

    @classmethod
    def clean_utterance(cls, utterance):
        """Clean the utterance.

        Returns: str
        """
        return CHATUtteranceCleaner.clean(utterance)

    @classmethod
    def clean_timestamp(cls, timestamp):
        """Clean the time stamp.

        Returns: str
        """
        return unify_timestamp(timestamp)

    @staticmethod
    def clean_translation(translation):
        """Clean the translation.

        No cleaning by default.

        Returns: str
        """
        return translation

    @classmethod
    def clean_word(cls, word):
        """Clean the word.

        Returns: str
        """
        return CHATWordCleaner.clean(word)

    @staticmethod
    def clean_morph_tier(morph_tier):
        """Clean the morphology tier.

        Default cleaner for the segment, gloss and POS tiers.

        No cleaning by default.

        Returns: str
        """
        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        """Clean the segment tier.

        Returns: str
        """
        return cls.clean_morph_tier(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        """Clean the gloss tier.

        Returns: str
        """
        return cls.clean_morph_tier(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        """Clean the POS tier.

        Returns: str
        """
        return cls.clean_morph_tier(pos_tier)

    @staticmethod
    def clean_session_metadata(session_filename, date, media_filename):
        """Clean across session metadata.

        Mostly used for correcting session dates having the default date
        `1984-01-01`.

        No cleaning by default.

        Args:
            session_filename (str): The name of the session file.
            date (str): The session date.
            media_filename (str): The name of the media file.

        Returns:
            Tuple[str, str]: (date, media filename)
        """
        return date, media_filename

    @staticmethod
    def clean_speaker_metadata(
            session_filename, speaker_label, name, role, age,
            gender, language, birth_date, target_child):
        """Clean across speaker metadata.

        Mostly used for correcting speaker metadata so as to match the speakers
        across different sessions later.

        No cleaning by default.

        Args:
            session_filename (str): The name of the session file.
            speaker_label (str): Code/label of speaker.
            name (str): Full name of speaker.
            role (str): Role of speaker in relation to target child.
            age (str): The age of the speaker at the current session.
            gender (str): The gender of the speaker.
            language (str): The language of the speaker.
            birth_date (str): The birth date of the speaker.
            target_child (Tuple[str, str]): The label and name of the target
                child.

        Returns:
            Tuple[str, str, str, str, str, str, str]:
            (speaker_label, name, role, age, gender, language, birth_date)
        """
        return speaker_label, name, role, age, gender, language, birth_date

    @staticmethod
    def utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier):
        """Clean across utterance tiers.

        No cleaning by default.

        Returns:
            Tuple[str, str, str, str, str]:
            (actual_utt, target_utt, seg_tier, gloss_tier, pos_tier)
        """
        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

    @staticmethod
    def clean_morpheme_word(morpheme_word):
        """Clean the morpheme word.

        Default cleaner for the segment, gloss and POS words.

        No cleaning by default.

        Returns: str
        """
        return morpheme_word

    @classmethod
    def clean_seg_word(cls, seg_word):
        """Clean the segment word.

        Returns: str
        """
        return cls.clean_morpheme_word(seg_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """Clean the gloss word.

        Returns: str
        """
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        """Clean the POS tag word.

        Returns: str
        """
        return cls.clean_morpheme_word(pos_word)

    @staticmethod
    def clean_morpheme(morpheme):
        """Clean the morpheme.

        Default cleaner for the segment, gloss and POS.

        No cleaning by default.

        Returns: str
        """
        return morpheme

    @classmethod
    def clean_segment(cls, segment):
        """Clean the segment.

        Returns: str
        """
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss_raw(cls, gloss):
        """Clean the gloss.

        Returns: str
        """
        return cls.clean_morpheme(gloss)

    @classmethod
    def clean_gloss(cls, gloss):
        """Map original gloss to ACQDIV gloss."""
        return ''

    @classmethod
    def clean_pos_raw(cls, pos):
        """Clean the POS tag.

        Returns: str
        """
        return cls.clean_morpheme(pos)

    @classmethod
    def clean_pos(cls, pos):
        """Map original POS tag to ACQDIV POS tag."""
        return ''

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        """Map original POS tag to Universal Dependency POS tag."""
        return ''
