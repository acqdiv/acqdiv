from abc import ABC, abstractmethod


class CHATCleaner(ABC):
    """Interface for cleaning the ACQDIV (CHAT) corpora."""

    # ---------- metadata cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_date(date):
        """Clean the date.

        Prescribed format:
            year-month-day
            YYYY-MM-DD

        Returns: str
        """
        pass

    # ---------- utterance cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_utterance(utterance):
        """Clean the utterance.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_record_speaker_label(session_filename, speaker_label):
        """Clean the speaker label in a record.

        Returns:
            str: The cleaned speaker label.
        """
        pass

    # ---------- morphology tier cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_seg_tier(seg_tier):
        """Clean the segment tier.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_gloss_tier(gloss_tier):
        """Clean the gloss tier.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_pos_tier(pos_tier):
        """Clean the POS tier.

        Returns: str
        """
        pass

    # ---------- cross cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_session_metadata(session_filename, date, media_filename):
        """Clean across session metadata.

        Mostly used for correcting session dates having the default date
        `1984-01-01`.

        Args:
            session_filename (str): The name of the session file.
            date (str): The session date.
            media_filename (str): The name of the media file.

        Returns:
            Tuple[str, str]: (date, media filename)
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_speaker_metadata(
            session_filename, speaker_label, name, role,
            age, gender, language, birth_date, target_child):
        """Clean across speaker metadata.

        Mostly used for correcting speaker metadata so as to match the speakers
        across different sessions later in the postprocessor.

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
        pass

    @staticmethod
    @abstractmethod
    def utterance_cross_clean(
            raw_utt, actual_utt, target_utt, seg_tier, gloss_tier, pos_tier):
        """Clean across utterance tiers.

        Returns:
            Tuple[str, str, str, str, str]:
            (actual_utt, target_utt, seg_tier, gloss_tier, pos_tier)
        """
        pass

    # ---------- word cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_word(word):
        """Clean the word.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_seg_word(seg_word):
        """Clean the segment word.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_gloss_word(gloss_word):
        """Clean the gloss word.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_pos_word(pos_word):
        """Clean the POS tag word.

        Returns: str
        """
        pass

    # ---------- morpheme cleaning ----------

    @staticmethod
    @abstractmethod
    def clean_segment(segment):
        """Clean the segment.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_gloss(gloss):
        """Clean the gloss.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_pos(pos):
        """Clean the POS tag.

        Returns: str
        """
        pass
