import logging
from acqdiv.parsers.ToolboxReader import ToolboxReader
from acqdiv.parsers.metadata import Chat, Imdi


class ToolboxParser:
    """ Toolbox parser for Chintang, Indonesian, Russian, & potentially Dene
    """
    def __init__(self, config, file_path):
        """ Initialize a Toolbox parser

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            A Toolbox parser
        """
        self.config = config
        self.file_path = file_path
        self.logger = logging.getLogger('pipeline.' + __name__)

        # Session body for utterances, etc.
        self.session_file = ToolboxReader(self.config, self.file_path)

        # Metadata
        if self.config['metadata']['type'] == "xml":
            # Hack to get the separate metadata file paths for IMDIs
            temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
            self.metadata_file_path = temp.replace(".txt", ".xml")
            self.metadata_parser = Chat(self.config, self.metadata_file_path)
        elif self.config['metadata']['type'] == "imdi":
            temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
            self.metadata_file_path = temp.replace(".txt", ".imdi")
            self.metadata_parser = Imdi(self.config, self.metadata_file_path)
        else:
            assert 0, "Unknown metadata format type: "#  + format

        # check for missing metadata files?
        """
        if not os.path.isfile(self.metadata_file_path):
            print("MISSING FILE:", self.metadata_file_path)
            sys.exit(1)
        """
        # self.metadata_parser = Imdi(self.metadata_file_path)

    def get_session_metadata(self):
        """ Do toolbox-specific parsing of session metadata

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file

        Returns:
            Session metadata
        """
        # TODO: fix this to just session or just __attrs__ in the metadata parser
        # this is an ugly hack due to the Indonesian corpus (body=Toolbox, but meta=XML)
        if self.metadata_parser.__class__.__name__ == "Imdi":
            md = self.metadata_parser.metadata['session']
            try:
                md['media_type'] = (
                    self.metadata_parser.metadata['media']['mediafile']['type'])
            except KeyError:
                md['media_type'] = None
                self.logger.info('Session {} has no media type information'.format(
                   self.file_path))
            return md
        elif self.metadata_parser.__class__.__name__ == "Chat":
            return self.metadata_parser.metadata['__attrs__']
        else:
            assert 0, "Unknown metadata format type: "#  + format

    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db

        Returns:
            Ordered dictionary of speaker (participant) metadata
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def next_utterance(self):
        """ Yield session level utterance data:

        Returns:
             Ordered dictionary of config file record_tiers
        """
        for record in self.session_file:
            if record is None:
                raise StopIteration
            yield record

###############################################################################


class ChintangParser(ToolboxParser):
    pass

###############################################################################


class IndonesianParser(ToolboxParser):
    pass

###############################################################################


class RussianParser(ToolboxParser):
    pass

