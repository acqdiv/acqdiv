import re

from acqdiv.parsers.chat.readers.fileparser import CHATFileParser
from acqdiv.parsers.chat.readers.actual_target_utterance \
    import ActualTargetUtteranceExtractor
from acqdiv.parsers.chat.readers.sentence_type \
    import SentenceTypeExtractor


class CHATReader:
    """Methods for reading CHAT files."""

    def __init__(self, session_file):
        """Set the variables.
        chat (acqdiv.parsers.chat.model.CHAT): The chat instance.
        participant (acqdiv.parsers.chat.model.Participant): The current
            Participant
        record (acqdiv.parsers.chat.model.Record): The current record.
        """
        self.chat = CHATFileParser.parse(session_file)

        self.participant_iterator = iter(self.chat.participants)
        self.participant = None

        self.record_iterator = iter(self.chat.records)
        self.record = None

    # ---------- metadata ----------

    def get_session_date(self):
        """Get the date of the session.

        Returns: str
        """
        return self.chat.date

    def get_session_media_filename(self):
        """Get the the media file name of the session.

        Returns: str
        """
        return self.chat.media_filename

    def get_target_child(self):
        """Get the target child of the session.

        Returns:
            Tuple[str, str]: (label, name)
        """
        for code, p in self.chat.participants.items():
            if p.role == 'Target_Child':
                return code, p.name

        return '', ''

    # ---------- speaker ----------

    def load_next_speaker(self):
        """Load the data for the next speaker.

        Returns:
            bool: 1 if a new speaker could be loaded, otherwise 0.
        """
        try:
            code = next(self.participant_iterator)
            self.participant = self.chat.participants[code]
        except StopIteration:
            return 0

        return 1

    def get_speaker_age(self):
        """Get the age of the speaker.

        Returns: str
        """
        return self.participant.age

    def get_speaker_birthdate(self):
        """Get the birth date of the speaker.

        Returns: str
        """
        return self.participant.birth_date

    def get_speaker_gender(self):
        """Get the gender of the speaker.

        Returns: str
        """
        return self.participant.sex

    def get_speaker_label(self):
        """Get the label of the speaker.

        Returns: str
        """
        return self.participant.code

    def get_speaker_language(self):
        """Get the language of the speaker.

        Returns: str
        """
        return self.participant.language

    def get_speaker_name(self):
        """Get the name of the speaker.

        Returns: str
        """
        return self.participant.name

    def get_speaker_role(self):
        """Get the role of the speaker.

        Returns: str
        """
        return self.participant.role

    # ---------- record ----------

    def load_next_record(self):
        """Load the next record.

        Returns:
            bool: 1 if a new record could be loaded, otherwise 0.
        """
        try:
            self.record = next(self.record_iterator)
        except StopIteration:
            return 0

        return 1

    def get_uid(self):
        """Get the ID of the utterance.

        Returns: str
        """
        return str(self.record.uid)

    # ---------- main line ----------

    def get_utterance(self):
        """Get the utterance.

        Returns: str
        """
        return self.record.utterance

    def get_sentence_type(self):
        """Get the sentence type of the utterance.

        Returns: str
        """
        utterance = self.get_utterance()
        return SentenceTypeExtractor.get_sentence_type(utterance)

    def get_actual_utterance(self):
        """Get the actual form of the utterance.

        Returns: str
        """
        utterance = self.get_utterance()
        return ActualTargetUtteranceExtractor.to_actual_utterance(utterance)

    def get_target_utterance(self):
        """Get the target form of the utterance.

        Returns: str
        """
        utterance = self.get_utterance()
        return ActualTargetUtteranceExtractor.to_target_utterance(utterance)

    def get_record_speaker_label(self):
        """Get the label of the speaker of the utterance.

        Returns: str
        """
        return self.record.participant_code

    def get_start_time(self):
        """Get the start time of the utterance.

        Returns: str
        """
        return self.record.start_time

    def get_end_time(self):
        """Get the end time of the utterance.

        Returns: str
        """
        return self.record.end_time

    # ---------- dependent tiers ----------

    def get_addressee(self):
        """Get the addressee of the utterance.

        Returns: str
        """
        return self.record.dependent_tiers.get('add', '')

    def get_translation(self):
        """Get the translation of the utterance.

        Returns: str
        """
        return self.record.dependent_tiers.get('eng', '')

    def get_comments(self):
        """Get the comments of the utterance.

        Returns: str
        """
        comments = self.record.dependent_tiers.get('com', '')
        situation = self.record.dependent_tiers.get('sit', '')
        action = self.record.dependent_tiers.get('act', '')
        explanation = self.record.dependent_tiers.get('exp', '')
        fields = [comments, situation, action, explanation]

        return '; '.join((f for f in fields if f))

    def get_morph_tier(self):
        """Get the morphology tier.

        Per default, this is the 'mor'-tier.

        Returns:
            str: The content of the morphology tier.
        """
        return self.record.dependent_tiers.get('mor', '')

    def get_seg_tier(self):
        """Get the tier containing segments.

        Returns: str
        """
        return self.get_morph_tier()

    def get_gloss_tier(self):
        """Get the tier containing glosses.

        Returns: str
        """
        return self.get_morph_tier()

    def get_pos_tier(self):
        """Get the tier containing POS tags.

        Returns: str
        """
        return self.get_morph_tier()

    # ---------- words ----------

    @staticmethod
    def get_utterance_words(utterance):
        """Get the words of an utterance.

        Words are defined as units separated by a blank space.

        Args:
            utterance (str): The utterance.

        Returns:
            list: The words.
        """
        if utterance:
            return re.split(r'\s+', utterance)
        else:
            return []

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        return cls.get_utterance_words(morph_tier)

    @classmethod
    def get_seg_words(cls, seg_tier):
        """Get the words from the segment tier.

        Returns: list
        """
        return cls.get_morpheme_words(seg_tier)

    @classmethod
    def get_gloss_words(cls, gloss_tier):
        """Get the words from the gloss tier.

        Returns: list
        """
        return cls.get_morpheme_words(gloss_tier)

    @classmethod
    def get_pos_words(cls, pos_tier):
        """Get the words from the POS tag tier.

        Returns: list
        """
        return cls.get_morpheme_words(pos_tier)

    @staticmethod
    def get_word_language(word):
        """Get the language of the word.

        Returns: str
        """
        return ''

    @staticmethod
    def get_standard_form():
        """Get the standard form of the utterance.

        Returns:
            str: 'actual' or 'target'
        """
        return 'actual'

    # ---------- morphemes ----------

    @staticmethod
    def get_morphemes(morpheme_word):
        """Get morphemes of a word.

        Per default, morphemes are separated by a dash.

        Args:
            morpheme_word (str): Word consisting of morphemes.

        Returns:
            list: The morphemes of the word.
        """
        return morpheme_word.split('-')

    @classmethod
    def get_segments(cls, seg_word):
        """Get the segments from the segment word.

        Returns: list
        """
        return cls.get_morphemes(seg_word)

    @classmethod
    def get_glosses(cls, gloss_word):
        """Get the glosses from the gloss word.

        Returns: list
        """
        return cls.get_morphemes(gloss_word)

    @classmethod
    def get_poses(cls, pos_word):
        """Get the POS tags from the POS word.

        Returns: list
        """
        return cls.get_morphemes(pos_word)

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        """Get language of the morpheme.

        Returns: str
        """
        return ''

    @staticmethod
    def get_main_morpheme():
        """Get the main morpheme.

        The main morpheme is the one used for linking the words of the
        respective morphology tier to those of the utterance. In case of
        misalignments between the morphology tiers, only the main morphemes
        are kept, while those of the other morphology tiers are nulled.

        Returns:
            str: 'segment' or 'gloss'.
        """
        return 'gloss'

    @staticmethod
    def get_morpheme_type():
        return 'target'
