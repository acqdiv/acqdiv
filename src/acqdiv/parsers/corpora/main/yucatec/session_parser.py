from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.yucatec.reader import YucatecReader
from acqdiv.parsers.corpora.main.yucatec.cleaner import YucatecCleaner
from acqdiv.parsers.corpora.main.yucatec import tc_cleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


class YucatecSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/yucatec/resources/'
        'speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return YucatecReader(session_file)

    @staticmethod
    def get_cleaner():
        return YucatecCleaner()

    def parse(self):
        session = super().parse()
        tc_cleaner.clean(session)
        return session
