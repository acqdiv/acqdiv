from acqdiv.parsers.corpora.main.chintang.reader import ChintangReader
from acqdiv.parsers.toolbox.parser import ToolboxParser
from acqdiv.parsers.corpora.main.chintang.imdi_parser \
    import ChintangIMDIParser
from acqdiv.parsers.corpora.main.chintang.cleaner \
    import ChintangCleaner
from acqdiv.parsers.corpora.main.chintang import tc_cleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


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

    def parse(self):
        session = super().parse()
        tc_cleaner.clean(session)
        return session
