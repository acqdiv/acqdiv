from acqdiv.parsers.chat.CHATParser import CHATParser
from acqdiv.parsers.corpora.main.turkish.TurkishReader import TurkishReader
from acqdiv.parsers.corpora.main.turkish.TurkishCleaner import TurkishCleaner

from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


class TurkishSessionParser(CHATParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/turkish/resources/'
        'speaker_label2macro_role.csv'
    ))

    @staticmethod
    def get_reader(session_file):
        return TurkishReader(session_file)

    @staticmethod
    def get_cleaner():
        return TurkishCleaner()
