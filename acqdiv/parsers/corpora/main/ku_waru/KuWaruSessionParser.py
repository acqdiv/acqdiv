from acqdiv.parsers.corpora.main.ku_waru.KuWaruReader import KuWaruReader
from acqdiv.parsers.metadata.CMDIParser import CMDIParser
from acqdiv.parsers.toolbox.BaseToolboxParser import BaseToolboxParser


class KuWaruSessionParser(BaseToolboxParser):

    def get_record_reader(self):
        return KuWaruReader(self.toolbox_path)

    def get_metadata_reader(self):
        return CMDIParser(self.metadata_path)
