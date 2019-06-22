from acqdiv.parsers.corpora.main.indonesian.IndonesianReader import \
    IndonesianReader
from acqdiv.parsers.metadata.CHATParser import CHATParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class IndonesianParser(ToolboxParser):

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(self.config['paths']['sessions_dir'],
                                         self.config['paths']['metadata_dir'])
        metadata_file_path = temp.replace(".txt", ".xml")
        return CHATParser(metadata_file_path)

    def get_session_metadata(self):
        return self.metadata_reader.metadata['__attrs__']

    def get_record_reader(self):
        return IndonesianReader(self.toolbox_file)