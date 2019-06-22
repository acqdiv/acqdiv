from acqdiv.parsers.corpora.main.indonesian.IndonesianReader import \
    IndonesianReader
from acqdiv.parsers.metadata.CHATParser import CHATParser
from acqdiv.parsers.toolbox.BaseToolboxParser import BaseToolboxParser


class IndonesianSessionParser(BaseToolboxParser):

    def get_metadata_reader(self):
        return CHATParser(self.metadata_path)

    def get_session_metadata(self):
        return self.metadata_reader.metadata['__attrs__']

    def get_record_reader(self):
        return IndonesianReader(self.toolbox_path)
