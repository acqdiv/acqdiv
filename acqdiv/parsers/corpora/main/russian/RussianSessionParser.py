from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.metadata.IMDIParser import IMDIParser


class RussianSessionParser(ToolboxParser):

    def get_record_reader(self):
        return RussianReader(self.toolbox_path)

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)
