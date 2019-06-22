from acqdiv.parsers.corpora.main.ku_waru.KuWaruReader import KuWaruReader
from acqdiv.parsers.metadata.CMDIParser import CMDIParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class KuWaruParser(ToolboxParser):

    def get_record_reader(self):
        return KuWaruReader(self.toolbox_file)

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(self.config['paths']['sessions_dir'],
                                         self.config['paths']['metadata_dir'])
        metadata_file_path = temp.replace(".tbt", ".imdi")
        return CMDIParser(metadata_file_path)