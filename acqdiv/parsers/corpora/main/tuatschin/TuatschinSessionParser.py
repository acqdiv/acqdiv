from acqdiv.parsers.corpora.main.tuatschin.TuatschinReader import \
    TuatschinReader
from acqdiv.parsers.metadata.CMDIParser import CMDIParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class TuatschinSessionParser(ToolboxParser):

    def get_metadata_reader(self):
        return CMDIParser(self.metadata_path)

    def get_record_reader(self):
        return TuatschinReader(self.toolbox_path)
