from acqdiv.parsers.corpora.main.chintang.ChintangReader import ChintangReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class ChintangParser(ToolboxParser):

    def get_record_reader(self):
        return ChintangReader(self.toolbox_file)