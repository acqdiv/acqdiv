from acqdiv.parsers.corpora.main.tuatschin.TuatschinReader import \
    TuatschinReader
from acqdiv.parsers.metadata.CMDIParser import CMDIParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class TuatschinParser(ToolboxParser):

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(self.config['paths']['sessions_dir'],
                                         self.config['paths']['metadata_dir'])
        metadata_file_path = temp.replace(".tbt", ".imdi")
        return CMDIParser(self.config, metadata_file_path)

    def get_record_reader(self):
        return TuatschinReader(self.toolbox_file)