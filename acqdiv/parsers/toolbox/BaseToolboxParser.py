import logging

from acqdiv.parsers.toolbox.ToolboxParser \
    import ToolboxParser
from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser


class BaseToolboxParser(ToolboxParser):
    """Gathers all data for the DB for a given Toolbox session file.

    Uses the ToolboxReader for reading a toolbox file and IMDIParser or BaseCHATParser for
    reading the corresponding metadata file.
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
        self.metadata_path = metadata_path
        self.toolbox_path = toolbox_path
        self.logger = logging.getLogger('pipeline.' + __name__)

        # get record reader
        self.record_reader = self.get_record_reader()
        # get metadata reader
        self.metadata_reader = self.get_metadata_reader()

    def get_session_metadata(self):
        """Get the metadata of a session.

        Returns:
            dict: Session metadata.
        """
        # TODO: fix this to session or just __attrs__ in the metadata reader
        md = self.metadata_reader.metadata['session']
        try:
            md['media_type'] = (
                self.metadata_reader.metadata['media']['mediafile']['type'])
        except KeyError:
            md['media_type'] = None
            self.logger.info('Session {} has no media type information'.format(
               self.toolbox_path))
        return md

    def next_speaker(self):
        """Yield participants metadata for the Speaker table in the DB.

        Returns:
            OrderedDict: Speaker (participant) metadata.
        """
        for speaker in self.metadata_reader.metadata['participants']:
            yield speaker

    def next_utterance(self):
        """Yield session level utterance data.

        Returns:
             OrderedDict: Utterance data.
        """
        for record in self.record_reader:
            if record is None:
                raise StopIteration
            yield record
