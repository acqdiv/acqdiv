from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.SessionParser import SessionParser
from acqdiv.model.Session import Session
from acqdiv.model.Speaker import Speaker

import os


class ToolboxParser(SessionParser):
    """Gathers all data for the DB for a given Toolbox session file.

    Uses the ToolboxReader for reading a toolbox file and
    IMDIParser or CHATParser for reading the corresponding metadata file.
    """

    def get_record_reader(self):
        return ToolboxReader(self.toolbox_path)

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def __init__(self, toolbox_path, metadata_path):
        """Get toolbox and metadata readers.

        Args:
            toolbox_path (str): Path to the toolbox file.
            metadata_path (str): Path to the metadata file.
        """
        self.session = Session()

        self.metadata_path = metadata_path
        self.toolbox_path = toolbox_path

        # get record reader
        self.record_reader = self.get_record_reader()
        # get metadata reader
        self.metadata_reader = self.get_metadata_reader()

    def parse(self):
        """Get the session instance.

        Returns:
            acqdiv.model.Session.Session: The Session instance.
        """
        self.add_session_metadata()
        self.add_speakers()

        return self.session

    def add_session_metadata(self):
        """Add the metadata of a session."""
        md = self.metadata_reader.metadata['session']

        try:
            md['media_type'] = (
                self.metadata_reader.metadata['media']['mediafile']['type'])
        except KeyError:
            md['media_type'] = None

        self.session.source_id = os.path.splitext(
            os.path.basename(self.toolbox_path))[0]
        self.session.date = md.get('date', None)

    def add_speakers(self):
        """Add the speakers of a session."""
        for speaker_dict in self.metadata_reader.metadata['participants']:
            speaker = Speaker()
            speaker.birth_date = speaker_dict.get('birthdate', None)
            speaker.gender_raw = speaker_dict.get('sex', None)
            speaker.code = speaker_dict.get('code', None)
            speaker.age_raw = speaker_dict.get('age', None)
            speaker.role_raw = speaker_dict.get('role', None)
            speaker.name = speaker_dict.get('name', None)
            speaker.languages_spoken = speaker_dict.get('languages', None)

            self.session.speakers.append(speaker)

    def next_utterance(self):
        """Yield session level utterance data.

        Returns:
             OrderedDict: Utterance data.
        """
        for record in self.record_reader:
            if record is None:
                raise StopIteration
            yield record
