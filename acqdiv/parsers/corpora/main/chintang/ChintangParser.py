from acqdiv.parsers.corpora.main.chintang.ChintangReader import ChintangReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.corpora.main.chintang.ChintangIMDIParser \
    import ChintangIMDIParser


class ChintangParser(ToolboxParser):

    def get_record_reader(self):
        return ChintangReader(self.toolbox_file)

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(
            self.config['paths']['sessions_dir'],
            self.config['paths']['metadata_dir'])
        metadata_file_path = temp.replace(".txt", ".imdi")
        return ChintangIMDIParser(metadata_file_path)
