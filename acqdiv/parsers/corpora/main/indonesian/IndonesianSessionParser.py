from acqdiv.parsers.corpora.main.indonesian.IndonesianReader import \
    IndonesianReader
from acqdiv.parsers.metadata.CHATParser import CHATParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
import os


class IndonesianSessionParser(ToolboxParser):

    def get_metadata_reader(self):
        return CHATParser(self.metadata_path)

    def get_session_metadata(self):
        self.metadata_reader.metadata['__attrs__']['source_id'] = \
            os.path.splitext(os.path.basename(self.toolbox_path))[0]
        return self.metadata_reader.metadata['__attrs__']

    def get_record_reader(self):
        return IndonesianReader(self.toolbox_path)
