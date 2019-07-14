from acqdiv.parsers.corpora.main.chintang.ChintangReader import ChintangReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.corpora.main.chintang.ChintangIMDIParser \
    import ChintangIMDIParser
from acqdiv.parsers.corpora.main.chintang.ChintangCleaner \
    import ChintangCleaner


class ChintangSessionParser(ToolboxParser):

    def get_record_reader(self):
        return ChintangReader()

    def get_metadata_reader(self):
        return ChintangIMDIParser(self.metadata_path)

    def get_cleaner(self):
        return ChintangCleaner()
