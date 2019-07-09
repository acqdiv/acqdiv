from acqdiv.parsers.corpora.main.dene.DeneReader import DeneReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class DeneSessionParser(ToolboxParser):

    def get_record_reader(self):
        return DeneReader(self.toolbox_path)

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)
