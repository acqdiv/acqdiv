from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.sesotho.reader import SesothoReader
from acqdiv.parsers.corpora.main.sesotho.cleaner import SesothoCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


class SesothoSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/sesotho/resources/'
        'speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return SesothoReader(session_file)

    @staticmethod
    def get_cleaner():
        return SesothoCleaner()
