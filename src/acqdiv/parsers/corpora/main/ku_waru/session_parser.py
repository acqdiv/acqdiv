from acqdiv.parsers.corpora.main.ku_waru.reader import KuWaruReader
from acqdiv.parsers.corpora.main.ku_waru.cleaner import KuWaruCleaner
from acqdiv.parsers.metadata.cmdi_parser import CMDIParser
from acqdiv.parsers.toolbox.parser import ToolboxParser


class KuWaruSessionParser(ToolboxParser):

    def get_record_reader(self):
        return KuWaruReader()

    def get_metadata_reader(self):
        return CMDIParser(self.metadata_path)

    def get_cleaner(self):
        return KuWaruCleaner()
