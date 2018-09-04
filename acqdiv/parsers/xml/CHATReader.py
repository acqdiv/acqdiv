import re

from acqdiv.parsers.xml.interfaces import CorpusReaderInterface


class CHATReader:
    """Generic reader methods for a CHAT file."""

    @staticmethod
    def _replace_line_breaks(session):
        """Remove line breaks within record tiers or metadata fields.

        CHAT inserts a line break and a tab when a tier or field becomes too
        long. The line breaks are replaced by a blank space.

        Args:
            session (str): The session.

        Returns:
            str:  The session without line breaks in tiers and fields.
        """
        return session.replace('\n\t', ' ')

    # ---------- metadata ----------

    @classmethod
    def iter_metadata_fields(cls, session):
        """Iter all metadata fields of a session.

        Metadata fields start with @ followed by the key, colon, tab and its
        content. Line breaks within a field are automatically removed and
        replaced by a blank space.

        Args:
            session (str): The session.

        Yields:
            str: The next metadata field.
        """
        metadata_regex = re.compile(r'@.*?:\t')
        session = cls._replace_line_breaks(session)
        for match in re.finditer(r'[^\n]+', session):
            line = match.group()
            if metadata_regex.search(line):
                yield line

            # metadata section ends
            if line.startswith('*'):
                break

    @staticmethod
    def get_metadata_field(metadata_field):
        """Get the key and content of the metadata field.

        The key is the part within the @ and the colon. The content is the
        part after the tab.

        Args:
            metadata_field (str): The metadata field as returned by
                                  'iter_metadata_fields'.

        Returns:
            tuple: (key, content).
        """
        key, content = metadata_field.split(':\t')
        return key.lstrip('@'), content

    # ---------- @Media ----------

    @staticmethod
    def get_media_fields(media):
        """Get the fields of @Media.

        @Media can consist of three fields:
            - filename (without extension)
            - format (e.g. video)
            - comment (e.g. unlinked)

        The comment is optional and an empty string will be returned
        if missing.

        Args:
            media (str): @Media content.

        Returns:
            tuple: (filename, format, comment).
        """
        fields = media.split(', ')
        # if comment is missing
        if len(fields) == 2:
            return fields[0], fields[1], ''
        else:
            return tuple(fields)

    @staticmethod
    def get_media_filename(media_fields):
        return media_fields[0]

    @staticmethod
    def get_media_format(media_fields):
        return media_fields[1]

    @staticmethod
    def get_media_comment(media_fields):
        return media_fields[2]

    # ---------- @Participants ----------

    @staticmethod
    def iter_participants(participants):
        """Iter participants in @Participants.

        @Participants is a comma-separated list of participants.

        Args:
            participants (str): @Participants content.

        Yields:
            str: The next participant.
        """
        participants_regex = re.compile(r'\s*,\s*')
        for participant in participants_regex.split(participants):
            yield participant

    @staticmethod
    def get_participant_fields(participant):
        """Get the fields of a participant.

        A participant can consist of three fields:
            - ID
            - name
            - role

        Name and role can be missing in which case an empty string is returned.
        If only one field is missing, it is the name.

        Args:
            participant (str): A participant as returned by iter_participants.

        Returns:
            tuple: (label, name, role).
        """
        fields = participant.split(' ')
        # name and role is missing
        if len(fields) == 1:
            return fields[0], '', ''
        # name is missing
        if len(fields) == 2:
            return fields[0], '', fields[1]
        else:
            return tuple(fields)

    @staticmethod
    def get_participant_id(participant_fields):
        return participant_fields[0]

    @staticmethod
    def get_participant_name(participant_fields):
        return participant_fields[1]

    @staticmethod
    def get_participant_role(participant_fields):
        return participant_fields[2]

    # ---------- @ID ----------

    @staticmethod
    def get_id_fields(id_field):
        """Get the fields of @ID.

        @ID consists of the following fields: language, corpus, code, age,
        sex, group, SES, role, education, custom.

        Args:
            id_field (str): @ID content.

        Returns:
            tuple: (language, corpus, code, age, sex, group, SES, role,
                    education, custom)
        """
        return tuple(id_field[:-1].split('|'))

    @staticmethod
    def get_id_language(id_fields):
        return id_fields[0]

    @staticmethod
    def get_id_corpus(id_fields):
        return id_fields[1]

    @staticmethod
    def get_id_code(id_fields):
        return id_fields[2]

    @staticmethod
    def get_id_age(id_fields):
        return id_fields[3]

    @staticmethod
    def get_id_sex(id_fields):
        return id_fields[4]

    @staticmethod
    def get_id_group(id_fields):
        return id_fields[5]

    @staticmethod
    def get_id_ses(id_fields):
        return id_fields[6]

    @staticmethod
    def get_id_role(id_fields):
        return id_fields[7]

    @staticmethod
    def get_id_education(id_fields):
        return id_fields[8]

    @staticmethod
    def get_id_custom(id_fields):
        return id_fields[9]

    # ---------- Record ----------

    @classmethod
    def iter_records(cls, session):
        """Yield a record of the session.

        A record starts with '*speaker_label:\t' in CHAT. Line breaks within
        the main line and dependent tiers are automatically removed and
        replaced by a blank space.

        Yields:
            str: The next record.
        """
        session = cls._replace_line_breaks(session)
        rec_regex = re.compile(r'\*[A-Za-z0-9]{2,3}:\t.*?(?=\n\*|\n@End)',
                               flags=re.DOTALL)
        # iter all records
        for match in rec_regex.finditer(session):
            rec = match.group()
            yield rec

    # ---------- Main line ----------

    @classmethod
    def get_mainline(cls, rec):
        """Get the main line of the record.

        Args:
            rec (str): The record.

        Returns:
            str: The main line.
        """
        main_line_regex = re.compile(r'^\*.*')
        return main_line_regex.search(rec).group()

    @staticmethod
    def get_mainline_fields(main_line):
        """Get the fields from the main line.

        The main line consists of the speaker ID, utterance and start and end
        time. The start and end times are optional.

        Args:
            main_line (str): The main line.

        Returns:
            tuple: (speaker ID, utterance, start time, end time).
        """
        main_line_regex = re.compile(
            r'\*([A-Za-z0-9]{2,3}):\t(.*?)(\s*\D?(\d+)(_(\d+))?\D?$|$)')
        match = main_line_regex.search(main_line)
        label = match.group(1)
        utterance = match.group(2)

        if match.group(4):
            start = match.group(4)
        else:
            start = ''

        if match.group(6):
            end = match.group(6)
        else:
            end = ''

        return label, utterance, start, end

    @staticmethod
    def get_mainline_speaker_id(main_line_fields):
        return main_line_fields[0]

    @staticmethod
    def get_mainline_utterance(main_line_fields):
        return main_line_fields[1]

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
            return re.split('\s+', utterance)
        else:
            return []

    @staticmethod
    def get_utterance_terminator(utterance):
        terminator_regex = re.compile(r'([+/.!?"]*[!?.])(?=(\s*\[\+|$))')
        match = terminator_regex.search(utterance)
        if match:
            return match.group(1)
        else:
            return ''

    @staticmethod
    def get_mainline_start_time(main_line_fields):
        return main_line_fields[2]

    @staticmethod
    def get_mainline_end_time(main_line_fields):
        return main_line_fields[3]

    # ---------- dependent tiers ----------

    @staticmethod
    def iter_dependent_tiers(rec):
        """Iter the dependent tiers of a record.

        A dependent tier starts with '%'.

        Args:
            rec (str): The record.

        Yields:
            str: The next dependent tier.
        """
        dependent_tier_regex = re.compile(r'(?<=\n)%.*')
        for dependent_tier in dependent_tier_regex.finditer(rec):
            yield dependent_tier.group()

    @staticmethod
    def get_dependent_tier(dependent_tier):
        """Get the key and content of the dependent tier.

        The key is the part with the % and the colon. The content starts after
        the tab.

        Args:
            dependent_tier (str): The dependent tier as returned by
                                  iter_dependent_tiers.

        Returns:
            tuple: (key, content).
        """
        key, content = dependent_tier.split(':\t')
        return key.lstrip('%'), content


###############################################################################

class ACQDIVCHATReader(CHATReader, CorpusReaderInterface):
    """The customized and optimized reader for the ACQDIV pipeline.

    Implements the CorpusReaderInterface.
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
                for participant in self.iter_participants(content):
                    # set speakers - @Participants
                    p_fields = self.get_participant_fields(participant)
                    p_id = self.get_participant_id(p_fields)
                    if p_id not in self._speakers:
                        self._speakers[p_id] = {}
                    self._speakers[p_id]['participant'] = p_fields
                    speaker_labels.append(p_id)

                    # set target child
                    p_role = self.get_participant_role(p_fields)
                    if p_role == 'Target_Child':
                        self._target_child = p_id
            else:
                self._metadata[key] = content

        self._speaker_iterator = iter(speaker_labels)
        self._record_iterator = self.iter_records(session)

    # ---------- metadata ----------

    def get_session_date(self):
        return self._metadata.get('Date', '')

    def get_session_filename(self):
        media_field = self._metadata.get('Media', '')
        media_fields = self.get_media_fields(media_field)
        return self.get_media_filename(media_fields)

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
        return 'u' + str(self._uid)

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
        replacement_regex1 = re.compile(r'<(.*?)> \[: .*?\]')
        clean = replacement_regex1.sub(r'\1', utterance)
        # one scoped word
        replacement_regex2 = re.compile(r'(\S+) \[: .*?\]')
        return replacement_regex2.sub(r'\1', clean)

    @staticmethod
    def get_replacement_target(utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words with brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[: (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_actual(utterance):
        """Get the actual form of fragments.

        Coding in CHAT: word starting with &.
        Keeps the fragment, removes the & from the word.
        """
        fragment_regex = re.compile(r'&([^-=]\S+)')
        return fragment_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'&[^-=]\S+')
        return fragment_regex.sub('xxx', utterance)

    @staticmethod
    def get_retracing_actual(utterance):
        """Get the actual form of retracings.

        Coding in CHAT: [/], [//], [///], [/-]

        Removal of retracing markers.
        """
        # several scoped words
        retracing_regex1 = re.compile(r'<(.*?)> \[(/{1,3}|/-)\]')
        clean = retracing_regex1.sub(r'\1', utterance)
        # one scoped word
        retracing_regex2 = re.compile(r'(\S+) \[(/{1,3}|/-)\]')
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
        retracing_regex = re.compile(r'([^>\s]+) \[//\] (\S+)')
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

###############################################################################


class EnglishManchester1Reader(ACQDIVCHATReader):

    # TODO: move all corrections to cleaner/postprocessor

    @staticmethod
    def correct_speaker_name(name, label, role, target_child_name):
        """Correct speaker name.

        Corrections:
        - if target child = 'Carl' and speaker_label = 'FAT', set name to 'Ian'
        - if label = RAC, set name to Rachel
        - if name = 'Mother', change to [speaker_role of target_child_name]
        - if name = 'Father', change to [speaker_role of target_child_name]
        - if name = 'Grandfather', change to
            [speaker_role of target_child_name]
        - if name missing and label != INV
            set name to [speaker_role of target_child_name]
        """
        # order is important!
        if target_child_name == 'Carl' and label == 'FAT':
            return 'Ian'
        elif name in {'Mother', 'Father', 'Grandfather'}:
            return role + ' of ' + target_child_name
        elif name:
            return name
        else:
            if label == 'RAC':
                return 'Rachel'
            elif label != 'INV':
                return role + ' of ' + target_child_name
            else:
                return name

    def get_speaker_name(self):
        """Get speaker name."""
        name = super().get_speaker_name()
        label = self.get_speaker_label()
        role = self.get_speaker_role()
        target_child_name = self.get_participant_name(
            self._speakers[self._target_child]['participant'])

        return self.correct_speaker_name(name, label, role, target_child_name)

    @staticmethod
    def correct_speaker_label(label):
        """Correct speaker label.

        Corrections:
        - if label = DAD, change to 'FAT'
        """
        if label == 'DAD':
            return 'FAT'
        else:
            return label

    def get_speaker_label(self):
        label = super().get_speaker_label()
        return self.correct_speaker_label(label)

    def get_record_speaker_label(self):
        label = super().get_record_speaker_label()
        return self.correct_speaker_label(label)

    def get_translation(self):
        return self.get_utterance()

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:fra'):
            return 'French'
        elif word.endswith('@s:ita'):
            return 'Italian'
        else:
            return 'English'

    @staticmethod
    def iter_morphemes(morph_word):
        """Iter morphemes of a word.

        A word consists of word groups in the case of
            - compounds (marker: +)
            - clitics (marker: ~)

        A word group has the following structure:
        prefix#POS|stem&fusionalsuffix-suffix=gloss

        prefix: segment, no gloss (-> assign segment), no POS (-> assign 'pfx')
        stem: segment, gloss (either from '='-part or segment), POS
        suffix: no segment, gloss, no POS (-> assign 'sfx')

        For every component of the compound '=' is prepended to the part (e.g.
        'n|+n|apple+n|tree' -> '=apple', '=tree'). The POS tag of the whole
        compound is removed.

        Returns:
            tuple: (segment, gloss, pos).
        """
        morpheme_regex = re.compile(r'[^#]+#'
                                    r'|[^\-]+'
                                    r'|[\-][^\-]+')

        # split into word groups (in case of compound, clitic) (if applicable)
        word_groups = re.split(r'[+~]', morph_word)

        # check if word is a compound
        if word_groups[0].endswith('|'):
            # remove POS tag of the whole compound
            del word_groups[0]
            is_compound = True
        else:
            is_compound = False

        for word_group in word_groups:

            # get stem gloss and remove it from morpheme word
            match = re.search(r'(.+)=(\S+)$', word_group)
            if match:
                word_group = match.group(1)
                stem_gloss = match.group(2)
            else:
                stem_gloss = ''

            # iter morphemes
            for match in morpheme_regex.finditer(word_group):
                morpheme = match.group()

                # prefix
                if morpheme.endswith('#'):
                    pfx = morpheme.rstrip('#')
                    segment = pfx
                    gloss = segment
                    pos = 'pfx'
                # sfx
                elif morpheme.startswith('-'):
                    sfx = morpheme.lstrip('-')
                    segment = ''
                    gloss = sfx
                    pos = 'sfx'
                # stem
                else:
                    pos, segment = morpheme.split('|')
                    # take gloss from '='-part, otherwise the segment
                    if stem_gloss:
                        gloss = stem_gloss
                    else:
                        gloss = segment

                    # if it is a compound part
                    if is_compound:
                        # prepend '=' to segment
                        segment = '=' + segment

                yield segment, gloss, pos

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        if pos == 'L2':
            return 'L2'
        else:
            return 'English'

###############################################################################


class InuktitutReader(ACQDIVCHATReader):
    """Inferences for Inuktitut."""

    def get_start_time(self):
        return self._dependent_tiers.get('tim', '')

    def get_end_time(self):
        return ''

    @staticmethod
    def get_actual_alternative(utterance):
        """Get the actual form of alternatives.

        Coding in CHAT: [=? <words>]
        The actual form is the alternative given in brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[=\? (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_target_alternative(utterance):
        """Get the target form of alternatives.

        Coding in CHAT: [=? <words>]
        The target form is the original form.
        """
        # several scoped words
        alternative_regex1 = re.compile(r'<(.*?)> \[=\? .*?\]')
        clean = alternative_regex1.sub(r'\1', utterance)
        # one scoped word
        alternative_regex2 = re.compile(r'(\S+) \[=\? .*?\]')
        return alternative_regex2.sub(r'\1', clean)

    def get_actual_utterance(self):
        """Get the actual form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_actual_utterance()
        return self.get_actual_alternative(utterance)

    def get_target_utterance(self):
        """Get the target form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_target_utterance()
        return self.get_target_alternative(utterance)

    def get_morph_tier(self):
        return self._dependent_tiers.get('xmor', '')

    @staticmethod
    def iter_morphemes(word):
        """Iter POS tags, segments and glosses of a word.

        Morphemes are separated by a '+'. POS tags are on the left
        separated by a '|' from the segment. There may be several POS tags
        all separated by a '|'. The gloss is on the right separated from the
        segment by a '^'.

        Args:
            word (str): A morpheme word.

        Yields:
            tuple: The next POS tag, segment and gloss in the word.
        """
        morpheme_regex = re.compile(r'(.*)\|(.*?)\^(.*)')
        for morpheme in word.split('+'):
            match = morpheme_regex.search(morpheme)
            if match:
                yield match.group(1), match.group(2), match.group(3)
            else:
                yield '', '', ''

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for _, seg, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, _, gloss in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for pos, _, _ in cls.iter_morphemes(pos_word)]

    @staticmethod
    def get_morpheme_language(seg, gloss, pos):
        if seg.endswith('@e'):
            return 'English'
        else:
            return 'Inuktitut'

###############################################################################


class CreeReader(ACQDIVCHATReader):

    @staticmethod
    def get_main_morpheme():
        return 'segment'

    def get_seg_tier(self):
        return self._dependent_tiers.get('xtarmor', '')

    def get_gloss_tier(self):
        return self._dependent_tiers.get('xmormea', '')

    def get_pos_tier(self):
        return self._dependent_tiers.get('xmortyp', '')

    @staticmethod
    def get_morphemes(word):
        if word:
            return word.split('~')
        else:
            return []

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
        if gloss == 'Eng':
            return 'English'
        else:
            return 'Cree'


###############################################################################


class JapaneseMiiProReader(ACQDIVCHATReader):

    def get_morph_tier(self):
        return self._dependent_tiers.get('xtrn', '')

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        else:
            return 'Japanese'

    @staticmethod
    def iter_morphemes(morph_word):
        """Iter morphemes of a word.

        A word consists of word groups in the case of compounds (marker: +).

        A word group has the following structure:
        prefix#POS|stem&fusionalsuffix-suffix=gloss

        prefix: segment, no gloss, no POS (-> assign 'pfx')
        stem: segment, gloss, POS
        suffix: no segment, with gloss, without POS (-> assign 'sfx')

        For every component of the compound '=' is prepended to the part (e.g.
        'n|+n|apple+n|tree' -> '=apple', '=tree'). Both parts receive the same
        gloss. The POS tag of the whole compound is removed. There may be
        prefixes attached to the whole compound. There are no clitics.

        Suffixes with a colon are specially treated: If the part after the
        colon is not 'contr' (contraction), it denotes the segment of the
        suffix.

        Returns:
            tuple: (segment, gloss, pos).
        """
        morpheme_regex = re.compile(r'[^#]+#'
                                    r'|[^\-]+'
                                    r'|[\-][^\-]+')

        # get stem gloss and remove it from morpheme word
        match = re.search(r'(.+)=(\S+)$', morph_word)
        if match:
            morph_word = match.group(1)
            stem_gloss = match.group(2)
        else:
            stem_gloss = ''

        # split into word groups (i.e. into compound parts) (if applicable)
        word_groups = morph_word.split('+')

        # check if word is a compound
        if len(word_groups) > 1:
            # pop prefixes & the POS tag of the whole compound
            pfxs_cmppos = word_groups.pop(0)

            # iter prefixes preceding compound
            for pfx_match in re.finditer(r'[^#]+(?=#)', pfxs_cmppos):
                yield pfx_match.group(), '', 'pfx'

        for word_group in word_groups:

            # iter morphemes
            for match in morpheme_regex.finditer(word_group):
                morpheme = match.group()

                # prefix
                if morpheme.endswith('#'):
                    segment = morpheme.rstrip('#')
                    gloss = ''
                    pos = 'pfx'
                # sfx
                elif morpheme.startswith('-'):
                    sfx = morpheme.lstrip('-')
                    pos = 'sfx'
                    match = re.search(r'([^:]+)(:(.*))?', sfx)
                    # check for colon case
                    if match.group(2) and match.group(3) != 'contr':
                        segment = match.group(3)
                        gloss = match.group(1)
                    else:
                        segment = ''
                        gloss = sfx
                # stem
                else:
                    pos, segment = morpheme.split('|')
                    # if it is a compound part
                    if len(word_groups) > 1:
                        # prepend '=' to segment
                        segment = '=' + segment
                    gloss = stem_gloss

                yield segment, gloss, pos

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]


###############################################################################


class JapaneseMiyataReader(ACQDIVCHATReader):

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        elif word.endswith('@s:deu'):
            return 'German'
        else:
            return 'Japanese'


###############################################################################

class TurkishReader(ACQDIVCHATReader):

    def get_start_time(self):
        """Get the start time.

        It is located on the %tim tier.
        """
        time = self._dependent_tiers.get('tim', '')
        if not time:
            return ''
        else:
            time_regex = re.compile(r'([\d:]+)')
            return time_regex.search(time).group()

    def get_end_time(self):
        """Get the end time.

        It is located on the %tim tier and might be missing.
        """
        time = self._dependent_tiers.get('tim', '')
        if not time:
            return ''
        else:
            time_regex = re.compile(r'-([\d:]+)')
            match = time_regex.search(time)
            if match:
                return match.group(1)
            else:
                return ''

    def get_morph_tier(self):
        return self._dependent_tiers.get('xmor', '')

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        elif word.endswith('@s:deu'):
            return 'German'
        elif word.endswith('@s:rus'):
            return 'Russian'
        else:
            return 'Turkish'

    @staticmethod
    def iter_morphemes(word):
        """Iter morphemes of a word.

        Morphemes are separated by dashes.

        Structure: stemPOS:substemPOS|stem-suffixgloss&subsuffixgloss

        Stem: segment, no gloss, POS tag
        Suffix: no segment, gloss, no POS tag (-> assign 'sfx')
        No prefixes, the first morpheme is always the stem.
        """
        morphemes = word.split('-')

        # first morpheme is always stem
        stem = morphemes.pop(0)

        # some morpheme words are malformed, null them
        if '|' not in stem:
            stem_seg = '???'
            stem_pos = '???'
        else:
            stem_pos, stem_seg = stem.split('|')

        yield stem_seg, '', stem_pos

        # iter suffixes
        for suffix in morphemes:
            yield '', suffix, 'sfx'

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]


###############################################################################

class YucatecReader(ACQDIVCHATReader):

    def get_morph_tier(self):
        return self._dependent_tiers.get('xmor', '')

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        """Get morpheme words.

        Words are separated by blank spaces as well as & and + in the case of
        clitics.
        """
        if morph_tier:
            return re.split(r'\s+|&|\+', morph_tier)
        else:
            return []

    @staticmethod
    def iter_morphemes(word):
        """Iter morphemes of a word.

        Morphemes are separated by '#' (prefixes), ':' (suffixes) and '-'
        (unstructured morpheme).

        Glosses and POS tags may have sub glosses and POS tags with are
        separated from the main gloss/POS tag by ':'. This use can be
        distinguished from the morpheme-separating use by checking the strings
        to the left and right of the ':' – when they consist of nothing but
        uppercase letters and digits, they are sub glosses or POS tags;
        otherwise they belong to different morphemes.

        Morphemes containing a '|' are structured, whereas those not containing
        one are unstructured. The part to the left is either the gloss or the
        POS tag, while the part to the right is the segment. A word can be
        completely or partially unstructured. The rules are as follows:
        - Word completely unstructured: The morphemes are separated by dashes.
          The segment is filled, while the gloss and POS tag remain unfilled.
        - Prefixes:
            - structured: segment is right block, gloss is left block, POS tag
              is 'pfx'
            - unstructured (NOT ATTESTED!): segment is unfilled, morpheme is
              gloss, POS tag is 'pfx'
        - Stem:
            - structured: segment is right block, left block is POS tag if:
                '3PRON', 'ADJ', 'ADV', 'AUX', 'CLFR', 'CLFR.INAN', 'CONJ',
                'DEICT', 'DEM', 'DET', 'INT', 'INTERJ', 'N', 'N.PROP',
                'N:PROP', 'NUM', 'PREP', 'PTL', 'QUANT', 'S', 'V', 'V.AUX',
                'V:AUX', 'VI', 'V.INTRANS', 'VT', 'V.TRANS'
              otherwise it is a gloss
            - unstructured: if morpheme only consists of uppercase letters and
              digits, it is a gloss, otherwise it is a segment
        - Suffixes:
            - structured: segment is right block, gloss is left block, POS tag
              is 'sfx'
            - unstructured: segment is unfilled, morpheme is gloss, POS tag is
              'sfx'
        """
        # untranscribed word
        if word == 'xxx':
            yield '', '', ''
        # completely unstructured word
        elif not re.search(r'[:|]', word) and '-' in word:
            for morpheme in word.split('-'):
                seg = morpheme
                gloss = ''
                pos = ''
                yield seg, gloss, pos
        # fully or partially structured word
        else:
            morph_regex = re.compile(
                r'(?P<prefixes>.*#)?'
                r'((?P<stemleft>[0-9A-Z:]+)\|)?(?P<stemright>[^:\-]+)'
                r'(?P<suffixes>[:\-].+)?')

            match = morph_regex.fullmatch(word)

            # ----- prefixes -----

            # if there are prefixes
            if match.group('prefixes'):
                prefix_string = match.group('prefixes').rstrip('#')
                # iter prefixes
                for pfx in prefix_string.split('#'):
                    pfx_structured = re.search(r'(.*)\|(.+)', pfx)
                    # structured prefixes
                    if pfx_structured is not None:
                        seg = pfx_structured.group(2)
                        gloss = pfx_structured.group(1)
                        pos = 'pfx'
                    # unstructured prefixes, tends to be gloss
                    else:
                        seg = ''
                        gloss = pfx
                        pos = 'pfx'
                    yield seg, gloss, pos

            # ----- stem -----

            # structured stems
            if match.group('stemleft'):
                seg = match.group('stemright')
                stem_left = match.group('stemleft')
                # stems with lexical meaning with the following POS tags
                # TODO: recheck this list
                stem_poses = {
                    '3PRON', 'ADJ', 'ADV', 'AUX', 'CLFR', 'CLFR.INAN', 'CONJ',
                    'DEICT', 'DEM', 'DET', 'INT', 'INTERJ', 'N', 'N.PROP',
                    'N:PROP', 'NUM', 'PREP', 'PTL', 'QUANT', 'S', 'V', 'V.AUX',
                    'V:AUX', 'VI', 'V.INTRANS', 'VT', 'V.TRANS'}
                if stem_left in stem_poses:
                    gloss = ''
                    pos = stem_left
                else:
                    gloss = stem_left
                    pos = ''
            # unstructured stems
            else:
                stem_right = match.group('stemright')
                if re.fullmatch(r'[A-Z0-9]+', stem_right):
                    seg = ''
                    gloss = stem_right
                    pos = ''
                else:
                    seg = stem_right
                    gloss = ''
                    pos = ''

            yield seg, gloss, pos

            # ----- suffixes -----

            # if there are suffixes
            if match.group('suffixes'):
                suffix_string = match.group('suffixes').lstrip(':').lstrip('-')
                # iter suffixes
                for sfx in re.split(r'(?<![A-Z0-9]):|(?<!\|)-', suffix_string):
                    sfx_structured = re.search(r'(.*)\|-?(.+)', sfx)
                    # structured suffixes
                    if sfx_structured is not None:
                        seg = sfx_structured.group(2)
                        gloss = sfx_structured.group(1)
                        pos = 'sfx'
                    # unstructured suffixes: tends to be gloss
                    else:
                        seg = ''
                        gloss = sfx
                        pos = 'sfx'
                    yield seg, gloss, pos

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]


###############################################################################

class SesothoReader(ACQDIVCHATReader):
    """Class to implement Sesotho Reading methods.

    Normally the methods get_utterance(), get_actual_utterance() and
    get_target_utterance() extract the utterance from the mainline.
    In Sesotho there are many misalignments between the
    mainline-utterance and the morpheme-tiers. So instead the
    utterance (for all three methods) is created by joining morphemes to
    words and those to the utterance.
    """

    def _join_morph_to_utt(self):
        """Create the utterance by joining the morphemes to words.

        Morphemes are separated by hyphens. The hyphens are removed.
        """
        seg_tier = self.get_seg_tier()
        seg_words = seg_tier.split(' ')
        utt_words = []

        for w in seg_words:
            w = ''.join(w.split('-'))
            utt_words.append(w)

        return ' '.join(utt_words)

    def get_utterance(self):
        """Get the utterance, created by joined morphemes."""
        return self._join_morph_to_utt()

    def get_actual_utterance(self):
        """Get the actual utterance, created by joined morphemes."""
        return self._join_morph_to_utt()

    def get_target_utterance(self):
        """Get the target utterance, created by joined morphemes."""
        return self._join_morph_to_utt()

    def get_seg_tier(self):
        """Extract the segments tier and do cross-cleaning.

        Cross-cleaning has to be done from here for access to different
        tiers at the same time.
        """
        return self._dependent_tiers.get('gls', '')

    def get_gloss_tier(self):
        return self._dependent_tiers.get('cod', '')

    def get_pos_tier(self):
        return self._dependent_tiers.get('cod', '')

    @staticmethod
    def infer_poses(morph_word):
        """Infer the pos-tags for a morpheme word.

        Args:
            morph_word: str, the morphemes of a word
        Return:
            str, the pos-tags
        """
        if not morph_word:
            return []

        morphemes = morph_word.split('-')
        passed_stem = False
        poses = []

        for mor in morphemes:
            pos = ''
            # Check for prefixes and suffixes.
            if len(morphemes) == 1 or (re.search(r'(v|id)\^|\(\d', mor)
                                       or re.match(r'(aj$|nm$|ps\d+)', mor)):
                passed_stem = True
            elif not passed_stem:
                pos = 'pfx'
            elif passed_stem:
                pos = 'sfx'

            if pos != 'pfx' and pos != 'sfx':
                # Check for verbs: verbs have v^, one typo as s^.
                if re.search(r'[vs]\^', mor):
                    pos = 'v'

                # Check for nouns: nouns contains "(\d)" (default) or "ps/"
                elif re.search('\(\d+', mor) or re.search('^ps/', mor):
                    pos = 'n'

                # Check for words with nominal concord.
                elif re.search(r'^(d|lr|obr|or|pn|ps|sr)\d+', mor):
                    pos_match = re.search('^(d|lr|obr|or|pn|ps|sr)\d+', mor)
                    pos = pos_match.group(1)

                # Check for particles: mostly without a precise gloss.
                elif re.search(
                        (r'^(aj|av|cd|cj|cm|ht|ij|loc|lr|ng|nm|obr|or|pr|q|sr'
                         r'|wh)$'),
                        mor):
                    pos = mor

                # Check for free person markers.
                elif re.search(r'^sm\d+[sp]?$', mor):
                    pos = 'afx.detached'

                # Check for copulas.
                elif re.search(r'^cp|cp$', mor):
                    pos = 'cop'

                # Check for ideophones.
                elif re.search(r'id\^', mor):
                    pos = 'ideoph'

                # Check for meaningless and unclear words. Note that
                # "xxx" in the Sesotho coding tier is not the same as
                # CHAT "xxx" in the transcription tier - it does not
                # stand for words that could not be transcribed but for
                # words with unclear meaning.
                elif mor == 'word' or mor == 'xxx':
                    pos = 'none'
                else:
                    pos = '???'

            poses.append(pos)

        return poses

    @classmethod
    def iter_morphemes(cls, morph_word):
        """Iter morphemes of a morph. word (encoding gloss and pos).

        This method only returns glosses and poses, but not segments,
        since segments are on a different tier. They are retrieved
        directly by get_segments().

        Morphemes (stems and affixes) are separated by hyphens.

        Args:
            morph_word: str, the morphemes of a word
        Returns:
            tuple: (<empty_string>, gloss, pos).
        """
        if not morph_word:
            yield ('', '', '')
        else:
            poses = cls.infer_poses(morph_word)
            morphemes = morph_word.split('-')

            for i in range(len(morphemes)):
                yield ('', morphemes[i], poses[i])

    @classmethod
    def get_segments(cls, seg_word):
        return seg_word.split('-')

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]

    # TODO: decide if remove
    # @staticmethod
    # def get_morpheme_language(seg, gloss, pos):
    #     return 'Sesotho'
    #
    # @staticmethod
    # def get_word_language(word):
    #     return 'Sesotho'

###############################################################################


class NungonReader(ACQDIVCHATReader):

    # ---------- morphology tier ----------

    def get_seg_tier(self):
        """Get the segment tier.

        The name of the segment tier can be either 'xgls' or 'gls'. The former
        is more common.
        """
        for seg_tier_name in ['xgls', 'gls']:
            if seg_tier_name in self._dependent_tiers:
                return self._dependent_tiers[seg_tier_name]
        return ''

    def get_gloss_tier(self):
        return self._dependent_tiers.get('xcod', '')

    def get_pos_tier(self):
        return self._dependent_tiers.get('xcod', '')

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        """Get the morpheme words of the morphology tier.

        Morpheme words are normally separated by whitespaces. Clitics are
        separated by '=' and are split off in parsing as they correspond
        to independent words in the utterance.
        """
        if morph_tier:
            return re.split(r'\s+|=', morph_tier)
        else:
            return []

    # ---------- morphemes ----------

    @classmethod
    def get_segments(cls, seg_word):
        """Segments are separated by dashes."""
        if seg_word:
            return seg_word.split('-')
        else:
            return []

    @staticmethod
    def iter_gloss_pos(gloss_pos_word):
        """Iter glosses and POS tags of a word.

        Morphemes are separated by dashes ('-'). Stems have a POS tag which is
        prefixed to the gloss by a caret ('^'). Prefixes and suffixes have only
        explicit glosses. They receive the POS tag 'pfx' and 'sfx',
        respectively. Some words do not have a stem marker in which case all
        morphemes get only glosses but no POS tags assigned.

        Yields:
            tuple: (gloss, POS tag)
        """
        morphemes = gloss_pos_word.split('-')

        # check if there is a stem marker
        if '^' not in gloss_pos_word:
            for gloss in morphemes:
                yield gloss, ''
        else:
            stem_passed = False
            for morpheme in morphemes:
                # check if it is the stem
                if '^' in morpheme:
                    # match POS up to the last ^ (in case there are several ^)
                    match = re.search(r'(.*)\^(.*)', morpheme)
                    gloss = match.group(2)
                    pos = match.group(1)
                    stem_passed = True
                else:
                    gloss = morpheme
                    if stem_passed:
                        pos = 'sfx'
                    else:
                        pos = 'pfx'

                yield gloss, pos

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for gloss, _ in cls.iter_gloss_pos(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, pos in cls.iter_gloss_pos(pos_word)]

    @classmethod
    def get_morpheme_language(cls, seg, gloss, pos):
        """Get the morpheme language.

        The morpheme language is coded in the POS tag. If it starts with 'eng',
        the morpheme is English, if it starts with 'tp', the morpheme is Tok
        Pisin.
        """
        if pos.startswith('eng'):
            return 'English'
        elif pos.startswith('tp'):
            return 'Tok Pisin'
        else:
            return 'Nungon'
