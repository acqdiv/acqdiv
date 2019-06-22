import re

from acqdiv.parsers.chat.readers.CHATReader import CHATReader
from acqdiv.parsers.chat.readers.RawCHATReader import RawCHATReader


class BaseCHATReader(RawCHATReader, CHATReader):
    """The customized and optimized reader for the ACQDIV pipeline.

    Implements the CHATReader.
    """

    def __init__(self):
        """Set the variables.

        _target_child (str): label of the target child of the session
        _metadata (dict): {metadata_name: metadata_content}
        _speakers (dict): {speaker_id:
                                {id: (language, corpus, code, age,...),
                                 'participant: (code, name, role)}}
        _speaker (str): label of current speaker
        _speaker_iterator (iterator): yields labels of speakers
        _record_iterator (iterator): yields records of a session
        _uid (int) = utterance ID starting at 0
        _main_line_fields (tuple): speaker ID, utterance, start time, end time
        _dependent_tiers (dict): {dependent_tier_name: dependent_tier_content}
        """
        # general metadata
        self._target_child = None
        self._metadata = None

        # speaker
        self._speakers = None
        self._speaker = None
        self._speaker_iterator = None

        # record
        self._record_iterator = None
        self._uid = -1
        self._main_line_fields = None
        self._dependent_tiers = None

    def read(self, session_file):
        """Read the session file.

        Sets the following variables:
            - _target_child
            - _metadata
            - _speakers
            - _speaker_iterator
            - _record_iterator

        Args:
            session_file (file/file-like object): A CHAT file.
        """
        session = session_file.read()
        self._metadata = {}
        self._speakers = {}
        speaker_labels = []

        for metadata_field in self.iter_metadata_fields(session):
            key, content = self.get_metadata_field(metadata_field)

            if key == 'ID':
                # set speakers - @ID
                id_fields = self.get_id_fields(content)
                id_code = self.get_id_code(id_fields)
                if id_code not in self._speakers:
                    self._speakers[id_code] = {}
                self._speakers[id_code]['id'] = id_fields
            elif key == 'Participants':
                for pos, participant in enumerate(
                        self.iter_participants(content)):
                    # set speakers - @Participants
                    p_fields = self.get_participant_fields(participant)
                    p_id = self.get_participant_id(p_fields)
                    if p_id not in self._speakers:
                        self._speakers[p_id] = {}
                    self._speakers[p_id]['participant'] = p_fields
                    speaker_labels.append(p_id)

                    # set target child
                    if self._is_target_child(pos, *p_fields):
                        p_name = self.get_participant_name(p_fields)
                        self._target_child = (p_id, p_name)

            else:
                self._metadata[key] = content

        self._speaker_iterator = iter(speaker_labels)
        self._record_iterator = self.iter_records(session)

    @classmethod
    def _is_target_child(cls, pos, label, name, role):
        """Infer whether this is the target child.

        Per default uses the role (`Target_Child`) to infer it.

        Args:
            pos (int): Position at which speaker is listed.
            label (str): Label of speaker.
            name (str): Name of speaker.
            role (str): Role of speaker.

        Returns:
            bool: Is it the target child?
        """
        return role == 'Target_Child'

    # ---------- metadata ----------

    def get_session_date(self):
        return self._metadata.get('Date', '')

    def get_session_media_filename(self):
        media_field = self._metadata.get('Media', '')
        media_fields = self.get_media_fields(media_field)
        return self.get_media_filename(media_fields)

    def get_target_child(self):
        if self._target_child:
            return self._target_child

        return '', ''

    # ---------- speaker ----------

    def load_next_speaker(self):
        """Load the next speaker.

        Resets the following variables if a new speaker can be loaded:
            - _speaker_iterator
            - _speaker
        """
        try:
            speaker_id = next(self._speaker_iterator)
        except StopIteration:
            return 0
        else:
            self._speaker = self._speakers[speaker_id]
            return 1

    def get_speaker_age(self):
        return self.get_id_age(self._speaker['id'])

    def get_speaker_birthdate(self):
        speaker_id = self.get_participant_id(self._speaker['participant'])
        birth_of = 'Birth of ' + speaker_id
        return self._metadata.get(birth_of, '')

    def get_speaker_gender(self):
        return self.get_id_sex(self._speaker['id'])

    def get_speaker_label(self):
        return self.get_participant_id(self._speaker['participant'])

    def get_speaker_language(self):
        return self.get_id_language(self._speaker['id'])

    def get_speaker_name(self):
        return self.get_participant_name(self._speaker['participant'])

    def get_speaker_role(self):
        return self.get_participant_role(self._speaker['participant'])

    # ---------- record ----------

    def load_next_record(self):
        """Load the next record.

        Resets the following variables if a new record can be loaded:
            - _uid
            - _main_line_fields
            - _dependent_tiers
        """
        try:
            rec = next(self._record_iterator)
        except StopIteration:
            return 0
        else:
            self._uid += 1

            main_line = self.get_mainline(rec)
            self._main_line_fields = self.get_mainline_fields(main_line)

            self._dependent_tiers = {}
            for dependent_tier in self.iter_dependent_tiers(rec):
                key, content = self.get_dependent_tier(dependent_tier)
                self._dependent_tiers[key] = content
            return 1

    def get_uid(self):
        return str(self._uid)

    def get_addressee(self):
        return self._dependent_tiers.get('add', '')

    def get_translation(self):
        return self._dependent_tiers.get('eng', '')

    def get_comments(self):
        comments = self._dependent_tiers.get('com', '')
        situation = self._dependent_tiers.get('sit', '')
        action = self._dependent_tiers.get('act', '')
        explanation = self._dependent_tiers.get('exp', '')
        fields = [comments, situation, action, explanation]

        return '; '.join((f for f in fields if f))

    def get_record_speaker_label(self):
        return self.get_mainline_speaker_id(self._main_line_fields)

    def get_start_time(self):
        return self.get_mainline_start_time(self._main_line_fields)

    def get_end_time(self):
        return self.get_mainline_end_time(self._main_line_fields)

    # ---------- utterance ----------

    def get_utterance(self):
        return self.get_mainline_utterance(self._main_line_fields)

    @staticmethod
    def terminator2sentence_type(terminator):
        """Map utterance terminator to sentence type.

        Returns:
            str: The sentence type.
        """
        mapping = {'.': 'default',
                   '?': 'question',
                   '!': 'exclamation',
                   '+.': 'broken for coding',
                   '+...': 'trail off',
                   '+..?': 'trail off of question',
                   '+!?': 'question with exclamation',
                   '+/.': 'interruption',
                   '+/?': 'interruption of a question',
                   '+//.': 'self-interruption',
                   '+//?': 'self-interrupted question',
                   '+"/.': 'quotation follows',
                   '+".': 'quotation precedes'}

        return mapping.get(terminator, '')

    def get_sentence_type(self):
        utterance = self.get_mainline_utterance(self._main_line_fields)
        terminator = self.get_utterance_terminator(utterance)
        return self.terminator2sentence_type(terminator)

    # ---------- actual & target ----------

    @staticmethod
    def get_shortening_actual(utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: parentheses within word.
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(?<=\S)\(\S+?\)|\(\S+?\)(?=\S)')
        return shortening_regex.sub('', utterance)

    @staticmethod
    def get_shortening_target(utterance):
        """Get the target form of shortenings.

        Coding in CHAT: parentheses within word.
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(?<=\S)\((\S+?)\)|\((\S+?)\)(?=\S)')
        return shortening_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_replacement_actual(utterance):
        """Get the actual form of replacements.

        Coding in CHAT: [: <words>] .
        Keeps replaced words, removes replacing words with brackets.
        """
        # several scoped words
        replacement_regex1 = re.compile(r'<(.*?)> ?\[: .*?\]')
        clean = replacement_regex1.sub(r'\1', utterance)
        # one scoped word
        replacement_regex2 = re.compile(r'(\S+) ?\[: .*?\]')
        return replacement_regex2.sub(r'\1', clean)

    @staticmethod
    def get_replacement_target(utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words within brackets. If there
        is more than one replacing word, they are joined together by an
        underscore.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) ?\[: (.*?)\]')

        def x(match):
            return match.group(1).replace(' ', '_')

        return replacement_regex.sub(x, utterance)

    @staticmethod
    def get_fragment_actual(utterance):
        """Get the actual form of fragments.

        Coding in CHAT: word starting with &.
        Keeps the fragment, removes the & from the word.
        """
        fragment_regex = re.compile(r'(^|\s)&([^-=\s]\S*)')
        return fragment_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'(^|\s)&([^-=\s]\S*)')
        return fragment_regex.sub(r'\1xxx', utterance)

    @staticmethod
    def get_retracing_actual(utterance):
        """Get the actual form of retracings.

        Coding in CHAT: [/], [//], [///], [/-]

        Removal of retracing markers.
        """
        # several scoped words
        retracing_regex1 = re.compile(r'<(.*?)> ?\[(/{1,3}|/-)\]')
        clean = retracing_regex1.sub(r'\1', utterance)
        # one scoped word
        retracing_regex2 = re.compile(r'(\S+) ?\[(/{1,3}|/-)\]')
        return retracing_regex2.sub(r'\1', clean)

    @classmethod
    def get_retracing_target(cls, utterance):
        """Get the target form of retracings.

        Coding in CHAT: [/], [//], [///], [/-]

        Same treatment as the actual form, except for single-word
        corrections in which both the retraced and retracing part receive
        the retracing value, e.g. hui [//] hoi du -> hoi hoi du. Multiple words
        being corrected cannot be replaced by their target forms since the
        correcting part can be of variable length.
        """
        # single-word correction
        retracing_regex = re.compile(r'([^>\s]+) ?\[//\] (\S+)')
        utterance = retracing_regex.sub(r'\2 \2', utterance)
        return cls.get_retracing_actual(utterance)

    @classmethod
    def to_actual_utterance(cls, utterance):
        for actual_method in [cls.get_shortening_actual,
                              cls.get_fragment_actual,
                              cls.get_replacement_actual]:
            utterance = actual_method(utterance)

        return utterance

    def get_actual_utterance(self):
        utterance = self.get_mainline_utterance(self._main_line_fields)
        return self.to_actual_utterance(utterance)

    @classmethod
    def to_target_utterance(cls, utterance):
        for target_method in [cls.get_shortening_target,
                              cls.get_fragment_target,
                              cls.get_replacement_target]:
            utterance = target_method(utterance)

        return utterance

    def get_target_utterance(self):
        utterance = self.get_mainline_utterance(self._main_line_fields)
        return self.to_target_utterance(utterance)

    @staticmethod
    def get_standard_form():
        return 'actual'

    # ---------- morphology ----------

    @staticmethod
    def get_word_language(word):
        """No coding per default."""
        return ''

    @staticmethod
    def get_main_morpheme():
        """Per default the gloss tier."""
        return 'gloss'

    # ---------- morphology tiers ----------

    def get_morph_tier(self):
        """Get the morphology tier.

        Per default, this is the 'mor'-tier.

        Returns:
            str: The content of the morphology tier.
        """
        return self._dependent_tiers.get('mor', '')

    def get_seg_tier(self):
        return self.get_morph_tier()

    def get_gloss_tier(self):
        return self.get_morph_tier()

    def get_pos_tier(self):
        return self.get_morph_tier()

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        return cls.get_utterance_words(morph_tier)

    @classmethod
    def get_seg_words(cls, seg_tier):
        return cls.get_morpheme_words(seg_tier)

    @classmethod
    def get_gloss_words(cls, gloss_tier):
        return cls.get_morpheme_words(gloss_tier)

    @classmethod
    def get_pos_words(cls, pos_tier):
        return cls.get_morpheme_words(pos_tier)

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
        return cls.get_morphemes(seg_word)

    @classmethod
    def get_glosses(cls, gloss_word):
        return cls.get_morphemes(gloss_word)

    @classmethod
    def get_poses(cls, pos_word):
        return cls.get_morphemes(pos_word)

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        """No coding per default."""
        return ''
