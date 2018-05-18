class SessionParser:
    """Parser for a session."""

    def __init__(self, session_path):
        """Set the path of the session file."""
        self.session_path = session_path


class RecordParser(SessionParser):
    """Parser for records of a session."""
    pass


class CHATRecordParser(RecordParser):
    """Parser for CHAT records of a session."""

    def iter_records(self):
        """Yield a record of the CHAT file.

        A record starts with ``*speaker_label:\t`` in CHAT.

        Yields:
            dict: The next record in the CHAT file.
                Dictionary has the following keys:
                utterance
                speaker_label
                start
                end
                dependent_tier_name1
                dependent_tier_name2
                <further dependent tiers>
        """
        pass

    def add_main_line(self, record_dict, record_str):
        """Add the data from the main line.

        Sets the following keys: utterance, speaker_label, start, end

        Args:
            record_dict (dict): Where the data from the main line is added.
            record_str (str): The stringified record.

        """
        pass

    def add_speaker_label(self, record_dict, main_line):
        """Add the speaker label from the main line.

        Args:
            record_dict (dict): Where the speaker label is added.
            main_line (str): The stringified main line.

        """
        pass

    def add_start(self, record_dict, main_line):
        """Add the start time from the main line.

        Args:
            record_dict (dict): Where the start time is added.
            main_line (str): The stringified main line.

        """
        pass

    def add_end(self, record_dict, main_line):
        """Add the end time from the main line.

        Args:
            record_dict (dict): Where the end time is added.
            main_line (str): The stringified main line.

        """
        pass

    def add_dependent_tiers(self, record_dict, record_str):
        """Add all dependent tiers.

        Dependent tiers start with ``%tier_name:\t``.

        Args:
            record_dict (dict): Where the dependent tiers are added.
            record_str (str): The stringified record.

        """
        pass

    def add_dependent_tier(self, record_dict, dependent_tier):
        """Add the dependent tier.

        Args:
            record_dict (dict): Where the dependent tier is added.
            dependent_tier (str): The stringified dependent tier.
        """
        pass
