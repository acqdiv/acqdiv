from acqdiv.parsers.corpora.main.chintang.ChintangReader import ChintangReader
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.corpora.main.chintang.ChintangIMDIParser \
    import ChintangIMDIParser
from acqdiv.parsers.corpora.main.chintang.ChintangCleaner \
    import ChintangCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


class ChintangSessionParser(ToolboxParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/chintang/resources/speaker_label2macro_role.csv'
    ))

    def get_record_reader(self):
        return ChintangReader()

    def get_metadata_reader(self):
        return ChintangIMDIParser(self.metadata_path)

    def get_cleaner(self):
        return ChintangCleaner()
