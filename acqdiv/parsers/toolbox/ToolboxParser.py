import logging

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser


class ToolboxParser:
    """Gathers all data for the DB for a given Toolbox session file.

    Uses the ToolboxReader for reading a toolbox file and IMDIParser or CHATParser for
    reading the corresponding metadata file.
    """

    def get_record_reader(self):
        return ToolboxReader(self.toolbox_file)

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(self.config['paths']['sessions_dir'],
                                         self.config['paths']['metadata_dir'])
        metadata_file_path = temp.replace(".txt", ".imdi")
        return IMDIParser(self.config, metadata_file_path)

    def __init__(self, config, toolbox_path):
        """Get toolbox and metadata readers.

        Args:
            config (CorpusConfigParser): Corpus config ini file.
            toolbox_path (str): Path to the toolbox file.
        """
        self.config = config
        self.toolbox_file = toolbox_path
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
               self.toolbox_file))
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
