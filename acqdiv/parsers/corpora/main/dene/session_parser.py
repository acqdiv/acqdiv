from acqdiv.parsers.corpora.main.dene.reader import DeneReader
from acqdiv.parsers.metadata.imdi_parser import IMDIParser
from acqdiv.parsers.toolbox.parser import ToolboxParser
from acqdiv.parsers.corpora.main.dene.cleaner import DeneCleaner


class DeneSessionParser(ToolboxParser):

    def get_record_reader(self):
        return DeneReader()

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def get_cleaner(self):
        return DeneCleaner()
