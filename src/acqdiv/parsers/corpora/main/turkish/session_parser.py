from acqdiv.parsers.chat.parser import CHATParser
from acqdiv.parsers.corpora.main.turkish.reader import TurkishReader
from acqdiv.parsers.corpora.main.turkish.cleaner import TurkishCleaner

from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


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
