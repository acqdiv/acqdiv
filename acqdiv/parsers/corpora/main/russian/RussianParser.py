from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class RussianParser(ToolboxParser):

    def get_record_reader(self):
        return RussianReader(self.toolbox_file)