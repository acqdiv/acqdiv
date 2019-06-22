from acqdiv.parsers.corpora.main.qaqet.QaqetIMDIParser import QaqetIMDI
from acqdiv.parsers.corpora.main.qaqet.QaqetReader import QaqetReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser


class QaqetSessionParser(ToolboxParser):

    def get_record_reader(self):
        return QaqetReader(self.toolbox_file)

    def get_metadata_reader(self):
        temp = self.toolbox_file.replace(self.config['paths']['sessions_dir'],
                                         self.config['paths']['metadata_dir'])

        # remove the session number '_\d'
        metadata_file_path = temp[:-6] + '.imdi'

        return QaqetIMDI(metadata_file_path)
