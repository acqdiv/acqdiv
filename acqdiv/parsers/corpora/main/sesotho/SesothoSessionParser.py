from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.sesotho.SesothoReader import SesothoReader
from acqdiv.parsers.corpora.main.sesotho.SesothoCleaner import SesothoCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


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
