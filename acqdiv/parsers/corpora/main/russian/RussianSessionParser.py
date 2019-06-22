from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.toolbox.BaseToolboxParser import BaseToolboxParser
from acqdiv.parsers.metadata.IMDIParser import IMDIParser


class RussianSessionParser(BaseToolboxParser):

    def get_record_reader(self):
        return RussianReader(self.toolbox_path)

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)
