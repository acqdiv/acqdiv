from acqdiv.parsers.corpora.main.dene.DeneReader import DeneReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.corpora.main.dene.DeneCleaner import DeneCleaner


class DeneSessionParser(ToolboxParser):

    def get_record_reader(self):
        return DeneReader()

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def get_cleaner(self):
        return DeneCleaner()
