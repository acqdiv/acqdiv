from acqdiv.parsers.corpora.main.qaqet.QaqetIMDIParser import QaqetIMDI
from acqdiv.parsers.corpora.main.qaqet.QaqetReader import QaqetReader
from acqdiv.parsers.toolbox.BaseToolboxParser import BaseToolboxParser


class QaqetSessionParser(BaseToolboxParser):

    def get_record_reader(self):
        return QaqetReader(self.toolbox_path)

    def get_metadata_reader(self):
        return QaqetIMDI(self.metadata_path)