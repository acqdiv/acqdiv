from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.yucatec.YucatecReader import YucatecReader
from acqdiv.parsers.corpora.main.yucatec.YucatecCleaner import YucatecCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


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
