import itertools
import mmap
import re

from acqdiv.parsers.xml.interfaces import CorpusReaderInterface


class CHATReader:
    """Generic reader methods for a CHAT file."""

    # ---------- metadata ----------

    @staticmethod
    def iter_metadata_fields(session_path):
        """Iter all metadata fields of a session file.

        Metadata fields start with @ followed by the key, colon, tab and its
        content.

        Args:
            session_path (str): Path to the session file.

        Yields:
            str: The next metadata field.
        """
        metadata_regex = re.compile(r'@.*?:\t')
        with open(session_path, 'r') as f:
            for line in f:
                if metadata_regex.search(line):
                    yield line.rstrip('\n')

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
        participants_regex = re.compile(r' ?, ?')
        for participant in participants_regex.split(participants):
            yield participant

    @staticmethod
    def get_participant_fields(participant):
        """Get the fields of a participant.

        A participant can consist of three fields:
            - ID
            - name
            - role

        The name is optional and an empty string will be returned if missing.

        Args:
            participant (str): A participant as returned by iter_participants.

        Returns:
            tuple: (label, name, role).
        """
        fields = participant.split(' ')
        # if name is missing
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

    @staticmethod
    def _replace_line_breaks(rec):
        """Remove line breaks within the tiers of a record.

        CHAT inserts line breaks when the text of a main line or dependent
        tier becomes too long. The line breaks are replaced by a blank space.

        Args:
            rec (str): The record.

        Returns:
            str: Record without break lines within the tiers.
        """
        return rec.replace('\n\t', ' ')

    @classmethod
    def iter_records(cls, session_path):
        """Yield a record of the CHAT file.

        A record starts with '*speaker_label:\t' in CHAT. Line breaks within
        the main line and dependent tiers are automatically removed and
        replaced by a blank space.

        Yields:
            str: The next record.
        """
        # for utterance ID generation
        counter = itertools.count()
        cls._uid = next(counter)

        with open(session_path, 'rb') as f:
            # use memory-mapping of files
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            # create a record generator
            rec_generator = re.finditer(br'\*[A-Za-z0-9]{2,3}:\t', mm)

            # get start of first record
            rec_start_pos = next(rec_generator).start()

            # iter all records
            for rec in rec_generator:

                # get start of next record
                next_rec_start_pos = rec.start()

                # get the stringified record
                rec_str = mm[rec_start_pos:next_rec_start_pos].decode()

                # clean line_breaks
                rec_str = cls._replace_line_breaks(rec_str)

                yield rec_str

                cls._uid = next(counter)

                # set new start of record
                rec_start_pos = next_rec_start_pos

            # handle last record
            rec_str = mm[rec_start_pos:].decode()
            yield rec_str

            cls._uid = None

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
            r'\*([A-Za-z0-9]{2,3}):\t(.*[.!?])(( \[.*\])?(.*?(\d+)_(\d+))?)?')
        match = main_line_regex.search(main_line)
        label = match.group(1)
        utterance = match.group(2)

        if match.group(6):
            start = match.group(6)
        else:
            start = ''

        if match.group(7):
            end = match.group(7)
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

        Words are separated by a blank space.

        Args:
            utterance (str): The utterance.

        Returns:
            list: The words.
        """
        if utterance:
            return utterance.split(' ')
        else:
            return []

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

    def __init__(self, session_file_path):
        self.session_file = session_file_path

        # metadata fields
        self._metadata_fields = self.get_metadata_fields()

        # speaker fields
        self._speaker_iterator = self.get_speaker_iterator()
        self._participant_fields = None
        self._id_fields = None

        # record fields
        self._record_iterator = self.get_record_iterator()
        self._uid = -1
        self._main_line_fields = None
        self._dependent_tiers = None

    # ---------- metadata ----------

    def get_metadata_fields(self):
        """Get the metadata fields of a session.

        All metadata keys map to a string, except @ID which maps to a
        dictionary of speaker IDs which in turn map to tuple of the @IDs
        sub-fields.

        Returns:
            dict: {metadata key: metadata content}
        """
        metadata_fields = {}
        for metadata_field in self.iter_metadata_fields(self.session_file):
            key, content = self.get_metadata_field(metadata_field)

            if key == 'ID':
                if key not in metadata_fields:
                    metadata_fields['ID'] = {}

                id_fields = self.get_id_fields(content)
                speaker_id = self.get_id_code(id_fields)
                metadata_fields['ID'][speaker_id] = id_fields
            else:
                metadata_fields[key] = content

        return metadata_fields

    def get_session_date(self):
        return self._metadata_fields['Date']

    def get_session_filename(self):
        media_field = self._metadata_fields['Media']
        media_fields = self.get_media_fields(media_field)
        return self.get_media_filename(media_fields)

    # ---------- speaker ----------

    def get_speaker_iterator(self):
        """Get a speaker iterator.

        Returns:
            iterator(str): The participants from @Participants.
        """
        participants = self._metadata_fields['Participants']
        return self.iter_participants(participants)

    def load_next_speaker(self):
        """Load the next speaker.

        Resets the following variables if a new speaker can be loaded:
            - _participant_fields
            - _id_fields
        """
        try:
            participant = next(self._speaker_iterator)
        except StopIteration:
            return 0
        else:
            self._participant_fields = self.get_participant_fields(participant)
            participant_id = self.get_participant_id(self._participant_fields)
            self._id_fields = self._metadata_fields['ID'][participant_id]
            return 1

    def get_speaker_age(self):
        return self.get_id_age(self._id_fields)

    def get_speaker_birthdate(self):
        speaker_id = self.get_participant_id(self._participant_fields)
        birth_of = 'Birth of ' + speaker_id
        return self._metadata_fields.get(birth_of, '')

    def get_speaker_gender(self):
        return self.get_id_sex(self._id_fields)

    def get_speaker_label(self):
        return self.get_participant_id(self._participant_fields)

    def get_speaker_language(self):
        return self.get_id_language(self._id_fields)

    def get_speaker_name(self):
        return self.get_participant_name(self._participant_fields)

    def get_speaker_role(self):
        return self.get_participant_role(self._participant_fields)

    # ---------- record ----------

    def get_record_iterator(self):
        """Get a record iterator.

        Returns:
            iterator(str): The records.
        """
        return self.iter_records(self.session_file)

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
        return self._dependent_tiers.get('com', '')

    def get_record_speaker_label(self):
        return self.get_mainline_speaker_id(self._main_line_fields)

    def get_start_time(self):
        return self.get_mainline_start_time(self._main_line_fields)

    def get_end_time(self):
        return self.get_mainline_end_time(self._main_line_fields)

    # ---------- utterance ----------

    def get_utterance(self):
        return self.get_mainline_utterance(self._main_line_fields)

    def get_sentence_type(self):
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

        terminator_regex = re.compile(r'([+/.!?"]*[!?.])(?=( \[\+|$))')
        utterance = self.get_mainline_utterance(self._main_line_fields)
        match = terminator_regex.search(utterance)
        return mapping[match.group(1)]

    # ---------- actual & target ----------

    @staticmethod
    def get_shortening_actual(utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: parentheses within word.
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(\S*)\(\S+\)(\S*)')
        return shortening_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_shortening_target(utterance):
        """Get the target form of shortenings.

        Coding in CHAT: \w+(\w+)\w+ .
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(\S*)\((\S+)\)(\S*)')
        return shortening_regex.sub(r'\1\2\3', utterance)

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
        fragment_regex = re.compile(r'&(\S+)')
        return fragment_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'&\S+')
        return fragment_regex.sub('xxx', utterance)

    def get_actual_utterance(self):
        utterance = self.get_mainline_utterance(self._main_line_fields)
        for actual_method in [self.get_shortening_actual,
                              self.get_fragment_actual,
                              self.get_replacement_actual]:
            utterance = actual_method(utterance)

        return utterance

    def get_target_utterance(self):
        utterance = self.get_mainline_utterance(self._main_line_fields)
        for target_method in [self.get_shortening_target,
                              self.get_fragment_target,
                              self.get_replacement_target]:
            utterance = target_method(utterance)

        return utterance

    def get_standard_form(self):
        return 'actual'

    # ---------- morphology ----------

    def get_word_language(self, word):
        """No coding per default."""
        return ''

    def get_main_morph_tier(self):
        """Per default the gloss tier."""
        return 'gloss'

    def get_seg_tier(self):
        raise NotImplementedError

    def get_gloss_tier(self):
        raise NotImplementedError

    def get_pos_tier(self):
        raise NotImplementedError

    def get_seg_words(self, seg_tier):
        return self.get_utterance_words(seg_tier)

    def get_gloss_words(self, gloss_tier):
        return self.get_utterance_words(gloss_tier)

    def get_pos_words(self, pos_tier):
        return self.get_utterance_words(pos_tier)

    def get_segments(self, seg_word):
        raise NotImplementedError

    def get_glosses(self, gloss_word):
        raise NotImplementedError

    def get_poses(self, pos_word):
        raise NotImplementedError

    def get_morpheme_language(self, seg, gloss, pos):
        """No coding per default."""
        return ''


class InuktitutReader(ACQDIVCHATReader):
    """Inferences for Inuktitut."""

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

    def get_seg_tier(self):
        return self.get_morph_tier()

    def get_gloss_tier(self):
        return self.get_morph_tier()

    def get_pos_tier(self):
        return self.get_morph_tier()

    @staticmethod
    def iter_morphemes(word):
        """Iter POS tags, segments and glosses of a word.

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

    def get_segments(self, seg_word):
        return [seg for _, seg, _ in self.iter_morphemes(seg_word)]

    def get_glosses(self, gloss_word):
        return [gloss for _, _, gloss in self.iter_morphemes(gloss_word)]

    def get_poses(self, pos_word):
        return [pos for pos, _, _ in self.iter_morphemes(pos_word)]

    def get_morpheme_language(self, seg, gloss, pos):
        if seg.endswith('@e'):
            return 'English'
        else:
            return 'Inuktitut'


class CreeReader(ACQDIVCHATReader):
    def get_main_morph_tier(self):
        return 'segment'

    def get_seg_tier(self):
        return self._dependent_tiers.get('xtarmor', '')

    def get_gloss_tier(self):
        return self._dependent_tiers.get('xmormea', '')

    def get_pos_tier(self):
        return self._dependent_tiers.get('xmortyp', '')

    @staticmethod
    def get_morphemes(word):
        return word.split('~')

    def get_segments(self, seg_word):
        return self.get_morphemes(seg_word)

    def get_glosses(self, gloss_word):
        return self.get_morphemes(gloss_word)

    def get_poses(self, pos_word):
        return self.get_morphemes(pos_word)

    def get_morpheme_language(self, seg, gloss, pos):
        if gloss == 'Eng':
            return 'English'
        else:
            return 'Cree'
