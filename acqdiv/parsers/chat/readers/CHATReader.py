from abc import ABC, abstractmethod


class CHATReader(ABC):
    """Interface for reading the ACQDIV (CHAT) corpora."""
    
    @abstractmethod
    def read(self, session_file):
        """Read the session file."""
        pass

    # ---------- metadata ----------

    @abstractmethod
    def get_session_date(self):
        """Get the date of the session.

        Returns: str
        """
        pass

    @abstractmethod
    def get_session_media_filename(self):
        """Get the the media file name of the session.

        Returns: str
        """
        pass

    @abstractmethod
    def get_target_child(self):
        """Get the target child of the session.

        Returns:
            Tuple[str, str]: (label, name)
        """
        pass

    # ---------- speaker ----------

    @abstractmethod
    def load_next_speaker(self):
        """Load the data for the next speaker.

        Returns:
            bool: 1 if a new speaker could be loaded, otherwise 0.
        """
        pass

    @abstractmethod
    def get_speaker_age(self):
        """Get the age of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_birthdate(self):
        """Get the birth date of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_gender(self):
        """Get the gender of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_label(self):
        """Get the label of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_language(self):
        """Get the language of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_name(self):
        """Get the name of the speaker.

        Returns: str
        """
        pass

    @abstractmethod
    def get_speaker_role(self):
        """Get the role of the speaker.

        Returns: str
        """
        pass

    # ---------- record ----------

    @abstractmethod
    def load_next_record(self):
        """Load the next record.

        Returns:
            bool: 1 if a new record could be loaded, otherwise 0.
        """
        pass

    @abstractmethod
    def get_uid(self):
        """Get the ID of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_addressee(self):
        """Get the addressee of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_translation(self):
        """Get the translation of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_comments(self):
        """Get the comments of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_record_speaker_label(self):
        """Get the label of the speaker of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_start_time(self):
        """Get the start time of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_end_time(self):
        """Get the end time of the utterance.

        Returns: str
        """
        pass

    # ---------- utterance ----------

    @abstractmethod
    def get_utterance(self):
        """Get the utterance.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def get_standard_form():
        """Get the standard form of the utterance.

        Returns:
            str: 'actual' or 'target'
        """
        pass

    @abstractmethod
    def get_actual_utterance(self):
        """Get the actual form of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_target_utterance(self):
        """Get the target form of the utterance.

        Returns: str
        """
        pass

    @abstractmethod
    def get_sentence_type(self):
        """Get the sentence type of the utterance.

        Returns: str
        """
        pass

    # ---------- morphology ----------
    
    @staticmethod
    @abstractmethod
    def get_word_language(word):
        """Get the language of the word.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def get_main_morpheme():
        """Get the main morpheme.

        The main morpheme is the one used for linking the words of the
        respective morphology tier to those of the utterance. In case of
        misalignments between the morphology tiers, only the main morphemes
        are kept, while those of the other morphology tier are nulled.

        Returns:
            str: 'segment' or 'gloss'.
        """
        pass

    @abstractmethod
    def get_seg_tier(self):
        """Get the tier containing segments.

        Returns: str
        """
        pass

    @abstractmethod
    def get_gloss_tier(self):
        """Get the tier containing glosses.

        Returns: str
        """
        pass

    @abstractmethod
    def get_pos_tier(self):
        """Get the tier containing POS tags.

        Returns: str
        """
        pass

    @staticmethod
    @abstractmethod
    def get_seg_words(seg_tier):
        """Get the words from the segment tier.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_gloss_words(gloss_tier):
        """Get the words from the gloss tier.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_pos_words(pos_tier):
        """Get the words from the POS tag tier.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_segments(seg_word):
        """Get the segments from the segment word.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_glosses(gloss_word):
        """Get the glosses from the gloss word.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_poses(pos_word):
        """Get the POS tags from the POS word.

        Returns: list
        """
        pass

    @staticmethod
    @abstractmethod
    def get_morpheme_language(seg, gloss, pos):
        """Get language of the morpheme.

        Returns: str
        """
        pass
