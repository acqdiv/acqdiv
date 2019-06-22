from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.toolbox.BaseToolboxParser import BaseToolboxParser


class RussianSessionParser(BaseToolboxParser):

    def get_record_reader(self):
        return RussianReader(self.toolbox_file)