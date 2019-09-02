import re

from acqdiv.parsers.chat.model.chat import CHAT
from acqdiv.parsers.chat.model.participant import Participant
from acqdiv.parsers.chat.model.record import Record


class CHATFileParser:
    """Methods for creating a CHAT instance."""

    @classmethod
    def parse(cls, session_file):
        """Get a CHAT instance from a CHAT file.

        Args:
            session_file (file/file-like object): A CHAT file.

        Returns:
            CHAT: The CHAT instance.
        """
        chat = CHAT()
        session = session_file.read()
        cls.add_headers(chat, session)
        cls.add_records(chat, session)

        return chat

    @classmethod
    def add_headers(cls, chat, session):
        """Add all headers to the CHAT instance.

        Args:
            chat (CHAT): The CHAT instance.
            session (str): The CHAT file as a string.
        """
        for metadata_field in cls.iter_metadata_fields(session):
            key, content = cls.get_metadata_field(metadata_field)

            if key == 'ID':
                id_fields = cls.get_id_fields(content)
                code = cls.get_id_code(id_fields)
                participant = chat.participants[code]
                participant.age = cls.get_id_age(id_fields)
                participant.language = cls.get_id_language(id_fields)
                participant.group = cls.get_id_group(id_fields)
                # do not overwrite role from @Participant
                if not participant.role:
                    participant.role = cls.get_id_role(id_fields)
                participant.corpus = cls.get_id_corpus(id_fields)
                participant.custom = cls.get_id_custom(id_fields)
                participant.education = cls.get_id_education(id_fields)
                participant.ses = cls.get_id_ses(id_fields)
                participant.sex = cls.get_id_sex(id_fields)

            elif key == 'Participants':
                for participant in cls.iter_participants(content):
                    p_fields = cls.get_participant_fields(participant)
                    participant = Participant()
                    participant.code = cls.get_participant_id(p_fields)
                    participant.role = cls.get_participant_role(p_fields)
                    participant.name = cls.get_participant_name(p_fields)
                    chat.participants[participant.code] = participant

            elif key == 'Media':
                media_fields = cls.get_media_fields(content)
                chat.media_format = cls.get_media_format(media_fields)
                chat.media_filename = cls.get_media_filename(media_fields)
                chat.media_comment = cls.get_media_comment(media_fields)

            elif key.startswith('Birth of'):
                _, _, participant_id = key.split(' ')
                chat.participants[participant_id].birth_date = content

            else:
                if hasattr(chat, key.lower()):
                    setattr(chat, key.lower(), content)

    @classmethod
    def add_records(cls, chat, session):
        """Add the records to the CHAT instance.

        Args:
            chat (CHAT): The CHAT instance.
            session (str): The CHAT file as a string.
        """
        uid = 0
        for rec_str in cls.iter_records(session):
            rec = Record()
            rec.uid = uid
            main_line = cls.get_mainline(rec_str)
            main_line_fields = cls.get_mainline_fields(main_line)
            rec.participant_code = cls.get_mainline_speaker_id(main_line_fields)
            rec.utterance = cls.get_mainline_utterance(main_line_fields)
            rec.start_time = cls.get_mainline_start_time(main_line_fields)
            rec.end_time = cls.get_mainline_end_time(main_line_fields)

            for dependent_tier in cls.iter_dependent_tiers(rec_str):
                key, content = cls.get_dependent_tier(dependent_tier)
                rec.dependent_tiers[key] = content

            chat.records.append(rec)
            uid += 1

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
        fields = re.split(r'\s+', participant)
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
        try:
            key, content = dependent_tier.split(':\t')
        # TODO: delete this once the source data (Inuktitut) is fixed
        except ValueError:
            key, content = dependent_tier.split(': ', maxsplit=1)

        return key.lstrip('%'), content
